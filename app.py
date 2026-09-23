from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger

from database import get_connection, init_db, TIPOS_ATIVIDADE, INTENSIDADES

app = Flask(__name__)
CORS(app)

app.config["SWAGGER"] = {
    "title": "API de Monitoramento de Atividades Físicas",
    "uiversion": 3,
}
swagger = Swagger(app, template={
    "info": {
        "title": "API de Monitoramento de Atividades Físicas",
        "description": "API REST para cadastro, consulta, edição e exclusão de atividades físicas.",
        "version": "1.0.0",
    }
})


def row_to_dict(row):
    return {
        "id": row["id"],
        "tipo": row["tipo"],
        "data": row["data"],
        "duracao": row["duracao"],
        "distancia": row["distancia"],
        "intensidade": row["intensidade"],
        "observacoes": row["observacoes"],
    }


def validar_atividade(dados, parcial=False):
    erros = []
    campos_obrigatorios = ["tipo", "data", "duracao", "intensidade"]

    if not parcial:
        for campo in campos_obrigatorios:
            if campo not in dados or dados[campo] in (None, ""):
                erros.append(f"O campo '{campo}' é obrigatório.")

    if "tipo" in dados and dados["tipo"] not in (None, "") and dados["tipo"] not in TIPOS_ATIVIDADE:
        erros.append(f"Tipo inválido. Valores aceitos: {', '.join(TIPOS_ATIVIDADE)}.")

    if "intensidade" in dados and dados["intensidade"] not in (None, "") and dados["intensidade"] not in INTENSIDADES:
        erros.append(f"Intensidade inválida. Valores aceitos: {', '.join(INTENSIDADES)}.")

    if "duracao" in dados and dados["duracao"] not in (None, ""):
        try:
            if int(dados["duracao"]) <= 0:
                erros.append("A duração deve ser um número inteiro positivo.")
        except (ValueError, TypeError):
            erros.append("A duração deve ser um número inteiro.")

    if dados.get("distancia") not in (None, ""):
        try:
            if float(dados["distancia"]) < 0:
                erros.append("A distância não pode ser negativa.")
        except (ValueError, TypeError):
            erros.append("A distância deve ser um número.")

    return erros


@app.route("/atividades", methods=["POST"])
def criar_atividade():
    """Cadastra uma nova atividade física
    ---
    tags:
      - Atividades
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [tipo, data, duracao, intensidade]
          properties:
            tipo:
              type: string
              example: Corrida
            data:
              type: string
              format: date
              example: 2026-09-13
            duracao:
              type: integer
              example: 45
            distancia:
              type: number
              example: 6.2
            intensidade:
              type: string
              example: Alta
            observacoes:
              type: string
              example: Treino pela manhã
    responses:
      201:
        description: Atividade criada com sucesso
      400:
        description: Dados inválidos
    """
    dados = request.get_json(silent=True) or {}
    erros = validar_atividade(dados)
    if erros:
        return jsonify({"erros": erros}), 400

    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO atividades (tipo, data, duracao, distancia, intensidade, observacoes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            dados["tipo"],
            dados["data"],
            int(dados["duracao"]),
            float(dados["distancia"]) if dados.get("distancia") not in (None, "") else None,
            dados["intensidade"],
            dados.get("observacoes"),
        ),
    )
    conn.commit()
    nova_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM atividades WHERE id = ?", (nova_id,)).fetchone()
    conn.close()

    return jsonify(row_to_dict(row)), 201


@app.route("/atividades", methods=["GET"])
def listar_atividades():
    """Retorna todas as atividades cadastradas
    ---
    tags:
      - Atividades
    responses:
      200:
        description: Lista de atividades
    """
    conn = get_connection()
    rows = conn.execute("SELECT * FROM atividades ORDER BY data DESC, id DESC").fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in rows]), 200


@app.route("/atividades/<int:atividade_id>", methods=["GET"])
def buscar_atividade(atividade_id):
    """Retorna uma atividade específica
    ---
    tags:
      - Atividades
    parameters:
      - in: path
        name: atividade_id
        type: integer
        required: true
    responses:
      200:
        description: Atividade encontrada
      404:
        description: Atividade não encontrada
    """
    conn = get_connection()
    row = conn.execute("SELECT * FROM atividades WHERE id = ?", (atividade_id,)).fetchone()
    conn.close()

    if row is None:
        return jsonify({"erro": "Atividade não encontrada."}), 404

    return jsonify(row_to_dict(row)), 200


@app.route("/atividades/<int:atividade_id>", methods=["PUT"])
def atualizar_atividade(atividade_id):
    """Atualiza uma atividade existente
    ---
    tags:
      - Atividades
    parameters:
      - in: path
        name: atividade_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            tipo:
              type: string
            data:
              type: string
              format: date
            duracao:
              type: integer
            distancia:
              type: number
            intensidade:
              type: string
            observacoes:
              type: string
    responses:
      200:
        description: Atividade atualizada
      400:
        description: Dados inválidos
      404:
        description: Atividade não encontrada
    """
    conn = get_connection()
    row = conn.execute("SELECT * FROM atividades WHERE id = ?", (atividade_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"erro": "Atividade não encontrada."}), 404

    dados = request.get_json(silent=True) or {}
    erros = validar_atividade(dados)
    if erros:
        conn.close()
        return jsonify({"erros": erros}), 400

    conn.execute(
        """
        UPDATE atividades
        SET tipo = ?, data = ?, duracao = ?, distancia = ?, intensidade = ?, observacoes = ?
        WHERE id = ?
        """,
        (
            dados["tipo"],
            dados["data"],
            int(dados["duracao"]),
            float(dados["distancia"]) if dados.get("distancia") not in (None, "") else None,
            dados["intensidade"],
            dados.get("observacoes"),
            atividade_id,
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM atividades WHERE id = ?", (atividade_id,)).fetchone()
    conn.close()

    return jsonify(row_to_dict(row)), 200


@app.route("/atividades/<int:atividade_id>", methods=["DELETE"])
def excluir_atividade(atividade_id):
    """Exclui uma atividade
    ---
    tags:
      - Atividades
    parameters:
      - in: path
        name: atividade_id
        type: integer
        required: true
    responses:
      204:
        description: Atividade excluída com sucesso
      404:
        description: Atividade não encontrada
    """
    conn = get_connection()
    row = conn.execute("SELECT * FROM atividades WHERE id = ?", (atividade_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"erro": "Atividade não encontrada."}), 404

    conn.execute("DELETE FROM atividades WHERE id = ?", (atividade_id,))
    conn.commit()
    conn.close()

    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
