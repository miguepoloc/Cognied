# %% [markdown]
# # Procesar datos del proyecto `DigitalMente`

# %% [markdown]
# ## **Encuesta de Ansiedad**
#
# Para esta encuesta se utilizaron los Baremos De Interpretación – Zung Self-Rating Anxiety Scale-15 (Zung, 1971
# Adaptada Por De Ávila, León-Valle Et Al., 2021).
#
# - 15-30 = **Ansiedad baja** = 1
# - 31-45 = **Ansiedad media** = 2
# - 46-60 = **Ansiedad alta** = 3
#

# %% [markdown]
# ## **Encuesta de Depresión**
#
# Para esta encuesta se utilizaron los Baremos De Interpretación – Escala del Centro de Estudios Epidemiológicos
# de La Depresión-10 (Kohout et al., 1993 validada Por Rueda-Jaimes Et Al., 2009)
#
# - 0-15 = **Sin síntomas depresivos** = 1
# - 15-30 = **Síntomas depresivos moderados** = 2
# - Mayor a 31 = **Síntomas depresivos graves** = 3
#

# %% [markdown]
# ## **Encuesta de Inteligencia Emocional**
#
# Para esta encuesta se utilizaron los Baremos De Interpretación – Escala de Inteligencia Emocional:
# TMMS-24 (Salovey y Vols. 1995 adaptado por Queiros et al., 2005)
#
# - _Factor I_. **Atención a las emociones** Se suman las preguntas de la 1 a la 8
# - _Factor II_. **Claridad de sentimientos** Se suman las preguntas de la 9 a la 16
# - _Factor III_. **Reparación del estado emocional** Se suman las preguntas de la 17 a la 24
#
# 1. **Atención**
#
# | Hombres                         | Mujeres                         | Categorización |
# | ------------------------------- | ------------------------------- | -------------- |
# | Presta poca atención: < 21      | Presta poca atención: < 24      | 1              |
# | Adecuada atención: 22 a 32      | Adecuada atención: 25 a 35      | 2              |
# | Presta demasiada atención: > 33 | Presta demasiada atención: > 36 | 3              |
#
# 2. **Claridad**
#
# | Hombres                           | Mujeres                            | Categorización |
# | --------------------------------- | ---------------------------------- | -------------- |
# | Debe mejorar su comprensión: < 25 | PDebe mejorar su comprensión: < 23 | 1              |
# | Adecuada comprensión: 26 a 35     | Adecuada comprensión: 24 a 34      | 2              |
# | Excelente comprensión: > 36       | Excelente comprensión: > 35        | 3              |
#
# 3. **Reparación**
#
# | Hombres                          | Mujeres                           | Categorización |
# | -------------------------------- | --------------------------------- | -------------- |
# | Debe mejorar su regulación: < 23 | PDebe mejorar su regulación: < 23 | 1              |
# | Adecuada regulación: 24 a 35     | Adecuada regulación: 24 a 34      | 2              |
# | Excelente regulación: > 36       | Excelente regulación: > 35        | 3              |
#

# %% [markdown]
# ## **Encuesta de Estrés Percibido**
#
# Para esta encuesta se utilizaron los Baremos De Interpretación – Escala de Estrés Percibido
# (Cohen et al. 1983 validada por Ruisoto et al., 2020).
#
# - 0-19 = **Estrés Bajo** = 1
# - 20-38 = **Estrés Medio** = 2
# - Mayor a 38 = **Estrés Alto** = 3
#


# ## **Encuesta de Pensamientos Automáticos**
#
# Para esta encuesta se utilizaron los Baremos De Interpretación – Inventario de Pensamientos Automáticos
# (Ruiz y Lujan, 1991)
#
# | Escala                           | Sumatoria de items | Bajo | Medio | Alto |
# | -------------------------------- | ------------------ | ---- | ----- | ---- |
# | Filtraje o abstracción selectiva | 1-16-31            | 0-3  | 4-6   | 7-9  |
# | Pensamiento polarizado           | 2-17-32            | 0-3  | 4-6   | 7-9  |
# | Sobregeneralización              | 3-18-33            | 0-3  | 4-6   | 7-9  |
# | Interpretación del pensamiento   | 4-19-34            | 0-3  | 4-6   | 7-9  |
# | Visión catastrófica              | 5-20-35            | 0-3  | 4-6   | 7-9  |
# | Personalización                  | 6-21-36            | 0-3  | 4-6   | 7-9  |
# | Falacia de control               | 7-22-37            | 0-3  | 4-6   | 7-9  |
# | Falacia de justicia              | 8-23-38            | 0-3  | 4-6   | 7-9  |
# | Razonamiento emocional           | 9-24-39            | 0-3  | 4-6   | 7-9  |
# | Falacia de cambio                | 10-25-40           | 0-3  | 4-6   | 7-9  |
# | Etiquetas globales               | 11-26-41           | 0-3  | 4-6   | 7-9  |
# | Culpabilidad                     | 12-27-42           | 0-3  | 4-6   | 7-9  |
# | Los deberías                     | 13-28-43           | 0-3  | 4-6   | 7-9  |
# | Tener razón                      | 14-29-44           | 0-3  | 4-6   | 7-9  |
# | Falacia de recompensa divina     | 15-30-45           | 0-3  | 4-6   | 7-9  |
#

# %% [markdown]
import pandas as pd


def calcular_ansiedad(dic_test, df_encuesta, tipo):
    """
    Calcula la ansiedad de un test
    """
    # Suma todas las respuestas y las guarda en ansiedad
    ansiedad = df_encuesta["id_pregunta_respuesta__id_respuesta__valor"].sum()
    # Recorre cada pregunta de la encuesta y guarda en un diccionario
    # el valor de cada pregunta
    for i in range(0, len(df_encuesta)):
        dic_test[tipo + "ansiedad" + str(i)] = df_encuesta.iloc[i]["id_pregunta_respuesta__id_respuesta__valor"]
    # Guarda el valor total del test en el diccionario
    dic_test[tipo + "ansiedad_total"] = ansiedad
    # Asigna la categoría correspondiente al test en el diccionario
    if ansiedad in range(15, 31):
        dic_test[tipo + "ansiedad_cat"] = 1
        dic_test[tipo + "ansiedad_text"] = "Ansiedad baja"
    elif ansiedad in range(31, 45):
        dic_test[tipo + "ansiedad_cat"] = 2
        dic_test[tipo + "ansiedad_text"] = "Ansiedad media"
    elif ansiedad in range(45, 60):
        dic_test[tipo + "ansiedad_cat"] = 3
        dic_test[tipo + "ansiedad_text"] = "Ansiedad alta"
    else:
        raise ValueError(f"El valor de ansiedad: {ansiedad} está fuera del rango")


def calcular_depresion(dic_test, df_encuesta, tipo):
    """
    Calcula la depresión de un test
    """
    # Suma los valores de las respuestas
    depresion = df_encuesta["id_pregunta_respuesta__id_respuesta__valor"].sum()
    # Guarda los valores de las respuestas en el diccionario
    for i in range(0, len(df_encuesta)):
        dic_test[tipo + "depresion" + str(i)] = df_encuesta.iloc[i]["id_pregunta_respuesta__id_respuesta__valor"]
    # Guarda el total de la depresion en el diccionario
    dic_test[tipo + "depresion_total"] = depresion
    # Categoriza el resultado de la depresion
    if depresion in range(0, 16):
        dic_test[tipo + "depresion_cat"] = 1
        dic_test[tipo + "depresion_text"] = "Sin síntomas depresivos"
    elif depresion in range(16, 31):
        dic_test[tipo + "depresion_cat"] = 2
        dic_test[tipo + "depresion_text"] = "Síntomas depresivos moderados"
    elif depresion in range(31, 60):
        dic_test[tipo + "depresion_cat"] = 3
        dic_test[tipo + "depresion_text"] = "Síntomas depresivos graves"
    else:
        raise ValueError(f"El valor de depresión: {depresion} está fuera del rango")


def processdata(query):
    # Leo el archivo json resultante de la consulta a la base de datos
    # query = "../data/subquery.json"
    df = pd.DataFrame(query)

    # Almaceno los id de los usuarios y las encuestas
    usuarios_id = df["id_usuario_encuesta__id_usuario__id"].unique()
    encuestas_id = df["id_usuario_encuesta__id_encuesta__id_encuesta"].unique()

    # Desarrollo de la función para calcular el puntaje de cada encuesta
    listadic = []
    for usuario in usuarios_id:
        df_filtrado_usuario = df.loc[df['id_usuario_encuesta__id_usuario__id'] == usuario]
        dic_test = {}
        for encuesta in encuestas_id:
            df_filtrado_encuesta = df_filtrado_usuario.loc[
                df['id_usuario_encuesta__id_encuesta__id_encuesta'] == encuesta
            ].sort_values("id_pregunta_respuesta__id_pregunta__itemid")
            id_encuesta = df_filtrado_encuesta["id_usuario_encuesta__id_usuario_encuesta"].unique()
            pretest = min(id_encuesta)
            posttest = max(id_encuesta)
            for tipo_test in id_encuesta:
                df_encuesta = df.loc[(df['id_usuario_encuesta__id_usuario_encuesta'] == tipo_test)].sort_values(
                    "id_pregunta_respuesta__id_pregunta__itemid"
                )
                dic_test["id_usuario"] = df_encuesta['id_usuario_encuesta__id_usuario__id'].unique()[0]
                dic_test["tipo_documento"] = df_encuesta['id_usuario_encuesta__id_usuario__tipo_documento'].unique()[0]
                dic_test["sexo"] = df_encuesta['id_usuario_encuesta__id_usuario__sexo__sexo'].unique()[0]
                dic_test["departamento"] = df_encuesta[
                    'id_usuario_encuesta__id_usuario__departamento_nacimiento'
                ].unique()[0]
                dic_test["ciudad"] = df_encuesta['id_usuario_encuesta__id_usuario__ciudad_nacimiento'].unique()[0]
                dic_test["fecha_nacimiento"] = df_encuesta[
                    'id_usuario_encuesta__id_usuario__fecha_nacimiento'
                ].unique()[0]
                dic_test["estado_civil"] = df_encuesta[
                    'id_usuario_encuesta__id_usuario__estado_civil__estado_civil'
                ].unique()[0]
                dic_test["facultad"] = df_encuesta[
                    'id_usuario_encuesta__id_usuario__programa_academico__facultad'
                ].unique()[0]
                dic_test["programa_academico"] = df_encuesta[
                    'id_usuario_encuesta__id_usuario__programa_academico__programa'
                ].unique()[0]
                dic_test["semestre"] = df_encuesta['id_usuario_encuesta__id_usuario__semestre'].unique()[0]
                dic_test["edad"] = df_encuesta['edad'].unique()[0]
                dic_test["covid_positivo"] = (
                    1 if df_encuesta['id_usuario_encuesta__id_usuario__covid_positivo'].unique()[0] else 0
                )
                dic_test["covid_familiar"] = (
                    1 if df_encuesta['id_usuario_encuesta__id_usuario__covid_familiar'].unique()[0] else 0
                )
                dic_test["covid_vacunado"] = (
                    1 if df_encuesta['id_usuario_encuesta__id_usuario__covid_vacuna'].unique()[0] else 0
                )
                dic_test["covid_tipo_vacuna"] = df_encuesta[
                    'id_usuario_encuesta__id_usuario__covid_tipo_vacuna'
                ].unique()[0]
                dic_test["covid_dosis_completa"] = (
                    1 if df_encuesta['id_usuario_encuesta__id_usuario__covid_dosis'].unique()[0] else 0
                )
                dic_test["discapacidad"] = (
                    1 if df_encuesta['id_usuario_encuesta__id_usuario__discapacidad'].unique()[0] else 0
                )
                if df_encuesta['id_usuario_encuesta__id_usuario__discapacidad_tipo'].unique()[0] is None:
                    dic_test["tipo_discapacidad"] = "No aplica"
                else:
                    dic_test["tipo_discapacidad"] = df_encuesta[
                        'id_usuario_encuesta__id_usuario__discapacidad_tipo'
                    ].unique()[0]
                dic_test["ocupacion"] = df_encuesta['id_usuario_encuesta__id_usuario__ocupacion'].unique()[0]
                dic_test["grupo_control"] = (
                    1 if df_encuesta['id_usuario_encuesta__id_usuario__is_controlgroup'].unique()[0] else 0
                )
                dic_test["administrador"] = (
                    1 if df_encuesta['id_usuario_encuesta__id_usuario__is_staff'].unique()[0] else 0
                )
                tipo = ""
                if tipo_test == pretest:
                    tipo = "pre_"
                elif tipo_test == posttest:
                    tipo = "post_"
                if encuesta == 3:
                    calcular_ansiedad(dic_test, df_encuesta, tipo)
                elif encuesta == 4:
                    calcular_depresion(dic_test, df_encuesta, tipo)
                elif encuesta == 5:
                    inteligencia_emocional = df_encuesta["id_pregunta_respuesta__id_respuesta__valor"].sum()
                    atencion = df_encuesta["id_pregunta_respuesta__id_respuesta__valor"][:8].sum()
                    claridad = df_encuesta["id_pregunta_respuesta__id_respuesta__valor"][9:16].sum()
                    reparacion = df_encuesta["id_pregunta_respuesta__id_respuesta__valor"][17:24].sum()
                    for i in range(0, len(df_encuesta)):
                        dic_test[tipo + "inteligencia_emocional" + str(i)] = df_encuesta.iloc[i][
                            "id_pregunta_respuesta__id_respuesta__valor"
                        ]

                    dic_test[tipo + "inteligencia_emocional_total"] = inteligencia_emocional

                    if df_encuesta['id_usuario_encuesta__id_usuario__sexo__sexo'].unique()[0] == "Masculino":
                        dic_test[tipo + "inteligencia_emocional_atencion"] = atencion
                        if atencion in range(0, 22):
                            dic_test[tipo + "inteligencia_emocional_atencion_cat"] = 1
                            dic_test[tipo + "inteligencia_emocional_atencion_text"] = "Presta poca atención"
                        elif atencion in range(22, 33):
                            dic_test[tipo + "inteligencia_emocional_atencion_cat"] = 2
                            dic_test[tipo + "inteligencia_emocional_atencion_text"] = "Adecuada atención"
                        elif atencion in range(33, 60):
                            dic_test[tipo + "inteligencia_emocional_atencion_cat"] = 3
                            dic_test[tipo + "inteligencia_emocional_atencion_text"] = "Presta demasiada atención"

                        dic_test[tipo + "inteligencia_emocional_claridad"] = claridad
                        if claridad in range(0, 26):
                            dic_test[tipo + "inteligencia_emocional_claridad_cat"] = 1
                            dic_test[tipo + "inteligencia_emocional_claridad_text"] = "Debe mejorar su comprensión"
                        elif claridad in range(26, 36):
                            dic_test[tipo + "inteligencia_emocional_claridad_cat"] = 2
                            dic_test[tipo + "inteligencia_emocional_claridad_text"] = "Adecuada comprensión"
                        elif claridad in range(36, 60):
                            dic_test[tipo + "inteligencia_emocional_claridad_cat"] = 3
                            dic_test[tipo + "inteligencia_emocional_claridad_text"] = "Excelente comprensión"

                        dic_test[tipo + "inteligencia_emocional_reparacion"] = reparacion
                        if reparacion in range(0, 24):
                            dic_test[tipo + "inteligencia_emocional_reparacion_cat"] = 1
                            dic_test[tipo + "inteligencia_emocional_reparacion_text"] = "Debe mejorar su regulación"
                        elif reparacion in range(24, 36):
                            dic_test[tipo + "inteligencia_emocional_reparacion_cat"] = 2
                            dic_test[tipo + "inteligencia_emocional_reparacion_text"] = "Adecuada regulación"
                        elif reparacion in range(36, 60):
                            dic_test[tipo + "inteligencia_emocional_reparacion_cat"] = 3
                            dic_test[tipo + "inteligencia_emocional_reparacion_text"] = "Excelente regulación"
                    else:
                        dic_test[tipo + "inteligencia_emocional_atencion"] = atencion
                        if atencion in range(0, 25):
                            dic_test[tipo + "inteligencia_emocional_atencion_cat"] = 1
                            dic_test[tipo + "inteligencia_emocional_atencion_text"] = "Presta poca atención"
                        elif atencion in range(25, 36):
                            dic_test[tipo + "inteligencia_emocional_atencion_cat"] = 2
                            dic_test[tipo + "inteligencia_emocional_atencion_text"] = "Adecuada atención"
                        elif atencion in range(36, 60):
                            dic_test[tipo + "inteligencia_emocional_atencion_cat"] = 3
                            dic_test[tipo + "inteligencia_emocional_atencion_text"] = "Presta demasiada atención"

                        dic_test[tipo + "inteligencia_emocional_claridad"] = claridad
                        if claridad in range(0, 24):
                            dic_test[tipo + "inteligencia_emocional_claridad_cat"] = 1
                            dic_test[tipo + "inteligencia_emocional_claridad_text"] = "Debe mejorar su comprensión"
                        elif claridad in range(24, 35):
                            dic_test[tipo + "inteligencia_emocional_claridad_cat"] = 2
                            dic_test[tipo + "inteligencia_emocional_claridad_text"] = "Adecuada comprensión"
                        elif claridad in range(35, 60):
                            dic_test[tipo + "inteligencia_emocional_claridad_cat"] = 3
                            dic_test[tipo + "inteligencia_emocional_claridad_text"] = "Excelente comprensión"

                        dic_test[tipo + "inteligencia_emocional_reparacion"] = reparacion
                        if reparacion in range(0, 24):
                            dic_test[tipo + "inteligencia_emocional_reparacion_cat"] = 1
                            dic_test[tipo + "inteligencia_emocional_reparacion_text"] = "Debe mejorar su regulación"
                        elif reparacion in range(24, 35):
                            dic_test[tipo + "inteligencia_emocional_reparacion_cat"] = 2
                            dic_test[tipo + "inteligencia_emocional_reparacion_text"] = "Adecuada regulación"
                        elif reparacion in range(35, 60):
                            dic_test[tipo + "inteligencia_emocional_reparacion_cat"] = 3
                            dic_test[tipo + "inteligencia_emocional_reparacion_text"] = "Excelente regulación"
                elif encuesta == 6:
                    estres = df_encuesta["id_pregunta_respuesta__id_respuesta__valor"].sum()
                    for i in range(0, len(df_encuesta)):
                        dic_test[tipo + "estres" + str(i)] = df_encuesta.iloc[i][
                            "id_pregunta_respuesta__id_respuesta__valor"
                        ]
                    dic_test[tipo + "estres_total"] = estres
                    if estres in range(0, 20):
                        dic_test[tipo + "estres_cat"] = 1
                        dic_test[tipo + "estres_text"] = "Estrés bajo"
                    elif estres in range(20, 39):
                        dic_test[tipo + "estres_cat"] = 2
                        dic_test[tipo + "estres_text"] = "Estrés medio"
                    elif estres in range(39, 70):
                        dic_test[tipo + "estres_cat"] = 3
                        dic_test[tipo + "estres_text"] = "Estrés alto"
                elif encuesta == 7:
                    valor = df_encuesta["id_pregunta_respuesta__id_respuesta__valor"].tolist()

                    for i in range(0, len(df_encuesta)):
                        dic_test[tipo + "pensamientos_automaticos" + str(i)] = df_encuesta.iloc[i][
                            "id_pregunta_respuesta__id_respuesta__valor"
                        ]

                    filtraje = valor[0] + valor[15] + valor[30]
                    dic_test[tipo + "filtraje"] = filtraje
                    if filtraje in range(0, 4):
                        dic_test[tipo + "filtraje_cat"] = 1
                        dic_test[tipo + "filtraje_text"] = "Filtraje o abstracción selectiva bajo"
                    elif filtraje in range(4, 7):
                        dic_test[tipo + "filtraje_cat"] = 2
                        dic_test[tipo + "filtraje_text"] = "Filtraje o abstracción selectiva medio"
                    elif filtraje in range(7, 10):
                        dic_test[tipo + "filtraje_cat"] = 3
                        dic_test[tipo + "filtraje_text"] = "Filtraje o abstracción selectiva alto"

                    polarizado = valor[1] + valor[16] + valor[31]
                    dic_test[tipo + "polarizado"] = polarizado
                    if polarizado in range(0, 4):
                        dic_test[tipo + "polarizado_cat"] = 1
                        dic_test[tipo + "polarizado_text"] = "Pensamiento polarizado bajo"
                    elif polarizado in range(4, 7):
                        dic_test[tipo + "polarizado_cat"] = 2
                        dic_test[tipo + "polarizado_text"] = "Pensamiento polarizado medio"
                    elif polarizado in range(7, 10):
                        dic_test[tipo + "polarizado_cat"] = 3
                        dic_test[tipo + "polarizado_text"] = "Pensamiento polarizado alto"

                    sobregeneralizacion = valor[2] + valor[17] + valor[32]
                    dic_test[tipo + "sobregeneralizacion"] = sobregeneralizacion
                    if sobregeneralizacion in range(0, 4):
                        dic_test[tipo + "sobregeneralizacion_cat"] = 1
                        dic_test[tipo + "sobregeneralizacion_text"] = "Sobregeneralizacion bajo"
                    elif sobregeneralizacion in range(4, 7):
                        dic_test[tipo + "sobregeneralizacion_cat"] = 2
                        dic_test[tipo + "sobregeneralizacion_text"] = "Sobregeneralizacion medio"
                    elif sobregeneralizacion in range(7, 10):
                        dic_test[tipo + "sobregeneralizacion_cat"] = 3
                        dic_test[tipo + "sobregeneralizacion_text"] = "Sobregeneralizacion alto"

                    interpretacion = valor[3] + valor[18] + valor[33]
                    dic_test[tipo + "interpretacion"] = interpretacion
                    if interpretacion in range(0, 4):
                        dic_test[tipo + "interpretacion_cat"] = 1
                        dic_test[tipo + "interpretacion_text"] = "Interpretación del pensamiento bajo"
                    elif interpretacion in range(4, 7):
                        dic_test[tipo + "interpretacion_cat"] = 2
                        dic_test[tipo + "interpretacion_text"] = "Interpretación del pensamiento medio"
                    elif interpretacion in range(7, 10):
                        dic_test[tipo + "interpretacion_cat"] = 3
                        dic_test[tipo + "interpretacion_text"] = "Interpretación del pensamiento alto"

                    vision = valor[4] + valor[19] + valor[34]
                    dic_test[tipo + "vision"] = vision
                    if vision in range(0, 4):
                        dic_test[tipo + "vision_cat"] = 1
                        dic_test[tipo + "vision_text"] = "Visión catastrófica bajo"
                    elif vision in range(4, 7):
                        dic_test[tipo + "vision_cat"] = 2
                        dic_test[tipo + "vision_text"] = "Visión catastrófica medio"
                    elif vision in range(7, 10):
                        dic_test[tipo + "vision_cat"] = 3
                        dic_test[tipo + "vision_text"] = "Visión catastrófica alto"

                    personalizacion = valor[5] + valor[20] + valor[35]
                    dic_test[tipo + "personalizacion"] = personalizacion
                    if personalizacion in range(0, 4):
                        dic_test[tipo + "personalizacion_cat"] = 1
                        dic_test[tipo + "personalizacion_text"] = "Personalización bajo"
                    elif personalizacion in range(4, 7):
                        dic_test[tipo + "personalizacion_cat"] = 2
                        dic_test[tipo + "personalizacion_text"] = "Personalización medio"
                    elif personalizacion in range(7, 10):
                        dic_test[tipo + "personalizacion_cat"] = 3
                        dic_test[tipo + "personalizacion_text"] = "Personalización alto"

                    control = valor[6] + valor[21] + valor[36]
                    dic_test[tipo + "control"] = control
                    if control in range(0, 4):
                        dic_test[tipo + "control_cat"] = 1
                        dic_test[tipo + "control_text"] = "Falacia de control bajo"
                    elif control in range(4, 7):
                        dic_test[tipo + "control_cat"] = 2
                        dic_test[tipo + "control_text"] = "Falacia de control medio"
                    elif control in range(7, 10):
                        dic_test[tipo + "control_cat"] = 3
                        dic_test[tipo + "control_text"] = "Falacia de control alto"

                    justicia = valor[7] + valor[22] + valor[37]
                    dic_test[tipo + "justicia"] = justicia
                    if justicia in range(0, 4):
                        dic_test[tipo + "justicia_cat"] = 1
                        dic_test[tipo + "justicia_text"] = "Falacia de justicia bajo"
                    elif justicia in range(4, 7):
                        dic_test[tipo + "justicia_cat"] = 2
                        dic_test[tipo + "justicia_text"] = "Falacia de justicia medio"
                    elif justicia in range(7, 10):
                        dic_test[tipo + "justicia_cat"] = 3
                        dic_test[tipo + "justicia_text"] = "Falacia de justicia alto"

                    razonamiento = valor[8] + valor[23] + valor[38]
                    dic_test[tipo + "razonamiento"] = razonamiento
                    if razonamiento in range(0, 4):
                        dic_test[tipo + "razonamiento_cat"] = 1
                        dic_test[tipo + "razonamiento_text"] = "Razonamiento emocional bajo"
                    elif razonamiento in range(4, 7):
                        dic_test[tipo + "razonamiento_cat"] = 2
                        dic_test[tipo + "razonamiento_text"] = "Razonamiento emocional medio"
                    elif razonamiento in range(7, 10):
                        dic_test[tipo + "razonamiento_cat"] = 3
                        dic_test[tipo + "razonamiento_text"] = "Razonamiento emocional alto"

                    cambio = valor[9] + valor[24] + valor[39]
                    dic_test[tipo + "cambio"] = cambio
                    if cambio in range(0, 4):
                        dic_test[tipo + "cambio_cat"] = 1
                        dic_test[tipo + "cambio_text"] = "Falacia de cambio bajo"
                    elif cambio in range(4, 7):
                        dic_test[tipo + "cambio_cat"] = 2
                        dic_test[tipo + "cambio_text"] = "Falacia de cambio medio"
                    elif cambio in range(7, 10):
                        dic_test[tipo + "cambio_cat"] = 3
                        dic_test[tipo + "cambio_text"] = "Falacia de cambio alto"

                    etiquetas = valor[10] + valor[25] + valor[40]
                    dic_test[tipo + "etiquetas"] = etiquetas
                    if etiquetas in range(0, 4):
                        dic_test[tipo + "etiquetas_cat"] = 1
                        dic_test[tipo + "etiquetas_text"] = "Falacia de etiquetas bajo"
                    elif etiquetas in range(4, 7):
                        dic_test[tipo + "etiquetas_cat"] = 2
                        dic_test[tipo + "etiquetas_text"] = "Falacia de etiquetas medio"
                    elif etiquetas in range(7, 10):
                        dic_test[tipo + "etiquetas_cat"] = 3
                        dic_test[tipo + "etiquetas_text"] = "Falacia de etiquetas alto"

                    culpabilidad = valor[11] + valor[26] + valor[41]
                    dic_test[tipo + "culpabilidad"] = culpabilidad
                    if culpabilidad in range(0, 4):
                        dic_test[tipo + "culpabilidad_cat"] = 1
                        dic_test[tipo + "culpabilidad_text"] = "Culpabilidad bajo"
                    elif culpabilidad in range(4, 7):
                        dic_test[tipo + "culpabilidad_cat"] = 2
                        dic_test[tipo + "culpabilidad_text"] = "Culpabilidad medio"
                    elif culpabilidad in range(7, 10):
                        dic_test[tipo + "culpabilidad_cat"] = 3
                        dic_test[tipo + "culpabilidad_text"] = "Culpabilidad alto"

                    deberias = valor[12] + valor[27] + valor[42]
                    dic_test[tipo + "deberias"] = deberias
                    if deberias in range(0, 4):
                        dic_test[tipo + "deberias_cat"] = 1
                        dic_test[tipo + "deberias_text"] = "Los deberías bajo"
                    elif deberias in range(4, 7):
                        dic_test[tipo + "deberias_cat"] = 2
                        dic_test[tipo + "deberias_text"] = "Los deberías medio"
                    elif deberias in range(7, 10):
                        dic_test[tipo + "deberias_cat"] = 3
                        dic_test[tipo + "deberias_text"] = "Los deberías alto"

                    tener_razon = valor[13] + valor[28] + valor[43]
                    dic_test[tipo + "tener_razon"] = tener_razon
                    if tener_razon in range(0, 4):
                        dic_test[tipo + "tener_razon_cat"] = 1
                        dic_test[tipo + "tener_razon_text"] = "Tener razón bajo"
                    elif tener_razon in range(4, 7):
                        dic_test[tipo + "tener_razon_cat"] = 2
                        dic_test[tipo + "tener_razon_text"] = "Tener razón medio"
                    elif tener_razon in range(7, 10):
                        dic_test[tipo + "tener_razon_cat"] = 3
                        dic_test[tipo + "tener_razon_text"] = "Tener razón alto"

                    recompensa = valor[14] + valor[29] + valor[44]
                    dic_test[tipo + "recompensa"] = recompensa
                    if recompensa in range(0, 4):
                        dic_test[tipo + "recompensa_cat"] = 1
                        dic_test[tipo + "recompensa_text"] = "Falacia de recompensa divina bajo"
                    elif recompensa in range(4, 7):
                        dic_test[tipo + "recompensa_cat"] = 2
                        dic_test[tipo + "recompensa_text"] = "Falacia de recompensa divina medio"
                    elif recompensa in range(7, 10):
                        dic_test[tipo + "recompensa_cat"] = 3
                        dic_test[tipo + "recompensa_text"] = "Falacia de recompensa divina alto"
                else:
                    pass
        listadic.append(dic_test)

    resultado = pd.DataFrame(listadic)
    # resultado_fin = resultado.to_json(orient="records")

    # Se guarda el resultado en un archivo excel
    resultado.to_excel("resultado.xlsx", index=False)

    return listadic
