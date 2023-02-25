SELECT e.id_encuesta,
    e.nombre AS "nombre_encuesta",
    ue.fecha,
    ue.id_usuario_encuesta,
    u.id,
    u.nombre,
    p.itemID,
    p.pregunta,
    r.valor,
    r.respuesta
FROM authentication_usuarios u
    INNER JOIN usuario_encuesta ue ON u.id = ue.id_usuario
    INNER JOIN api_avancemodulos api_avance ON u.id = api_avance.usuario_id
    INNER JOIN encuesta e ON e.id_encuesta = ue.id_encuesta
    INNER JOIN usuario_respuesta ur ON ue.id_usuario_encuesta = ur.id_usuario_encuesta
    INNER JOIN pregunta_respuesta pr ON ur.id_pregunta_respuesta = pr.id_pregunta_respuesta
    INNER JOIN pregunta p ON pr.id_pregunta = p.id_pregunta
    INNER JOIN respuesta r ON pr.id_respuesta = r.id_respuesta
WHERE e.id_encuesta = 3
    AND api_avance.autoevaluativo = 3
    AND ue.id_usuario_encuesta =(
        SELECT MIN(ue2.id_usuario_encuesta)
        FROM usuario_encuesta AS ue2
        WHERE ue2.id_usuario = ue.id_usuario
            AND ue2.id_encuesta = 3
    )
ORDER BY u.nombre,
    ue.id_usuario_encuesta,
    p.itemID ASC;