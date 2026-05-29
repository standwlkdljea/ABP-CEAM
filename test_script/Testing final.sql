-- =============================================================================
-- TEST 1: CASOS DE ÉXITO (INSERCIONES Y UNIÓN)
-- =============================================================================
USE vetcuidado_db;

-- Insertar usuario de prueba
INSERT INTO `usuarios` (`nombre_completo`, `dni`, `email`, `password_hash`, `telefono`) 
VALUES ('Test User', '99999999T', 'test.user@email.com', 'hash_test', '699999999');

-- Insertar mascota vinculada (Usamos LAST_INSERT_ID() para capturar dinámicamente el ID del dueño)
INSERT INTO `mascotas` (`nombre_mascota`, `tipo_mascota`, `edad`, `descripcion`, `id_usuario`)
VALUES ('Tester', 'Perro', 4, 'Perro de pruebas para DBeaver', LAST_INSERT_ID());

-- Comprobación de relación mediante JOIN
SELECT u.nombre_completo AS Dueno, m.nombre_mascota AS Mascota
FROM usuarios u
JOIN mascotas m ON u.id = m.id_usuario
WHERE u.dni = '99999999T';


-- =============================================================================
-- TEST 2: RESTRICCIONES DE INTEGRIDAD (ERRORES ESPERADOS)
-- =============================================================================

-- Error esperado: DNI duplicado (Unique Key)
INSERT INTO `usuarios` (`nombre_completo`, `dni`, `email`, `password_hash`, `telefono`) 
VALUES ('Otro Usuario', '99999999T', 'otro.email@email.com', 'hash', '600000000');

-- Error esperado: ID de usuario inexistente (Foreign Key)
INSERT INTO `mascotas` (`nombre_mascota`, `tipo_mascota`, `edad`, `id_usuario`)
VALUES ('Fantasma', 'Gato', 2, 99999);

-- Error esperado: Duplicar día de la semana (Unique Key en horarios_trabajo)
-- El día 0 (Lunes) ya fue insertado en la configuración inicial.
INSERT INTO `horarios_trabajo` (`dia_semana`, `hora_apertura`, `hora_cierre`) 
VALUES (0, '08:00:00', '14:00:00');


-- =============================================================================
-- TEST 3: ELIMINACIÓN EN CASCADA
-- =============================================================================

-- Borrar usuario y verificar propagación en mascotas (ON DELETE CASCADE)
DELETE FROM `usuarios` WHERE `dni` = '99999999T';

-- Debe devolver un resultado vacío (0 filas) porque 'Tester' se debió eliminar solo
SELECT * FROM `mascotas` WHERE `nombre_mascota` = 'Tester';


-- ==============================================================================
-- TEST 4: MÁS ERRORES ESPERADOS (CONSTRAINTS Y TIPOS DE DATOS)
-- ==============================================================================

-- Error esperado: Intentar crear un usuario sin DNI (Campo obligatorio / NOT NULL)
INSERT INTO `usuarios` (`nombre_completo`, `email`, `password_hash`) 
VALUES ('Usuario Incompleto', 'incompleto@email.com', 'hash_pass');

-- Error esperado: Tipo de dato incorrecto en la edad (String en campo INT)
-- Nota: Si el modo estricto de SQL está apagado, podría guardarlo como 0, 
-- pero con el modo estricto por defecto de MySQL fallará.
INSERT INTO `mascotas` (`nombre_mascota`, `tipo_mascota`, `edad`, `id_usuario`)
VALUES ('Mascota Rara', 'Gato', 'TRES AÑOS', 1);

-- Error esperado: Duración inválida (Violación de CHECK constraint > 0 en servicios)
INSERT INTO `servicios` (`nombre`, `duracion_minutos`, `descripcion`) 
VALUES ('Consulta Express', 0, 'Intento de servicio sin tiempo');

-- Error esperado: Horario inconsistente (Violación de CHECK hora_apertura < hora_cierre)
INSERT INTO `horarios_trabajo` (`dia_semana`, `hora_apertura`, `hora_cierre`) 
VALUES (6, '18:00:00', '09:00:00');