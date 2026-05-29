-- =============================================================================
-- TEST 1: CASOS DE ÉXITO (INSERCIONES Y UNIÓN)
-- =============================================================================
-- Insertar usuario de prueba
INSERT INTO `usuarios` (`nombre_completo`, `dni`, `email`, `password_hash`, `telefono`) 
VALUES ('Test User', '99999999T', 'test.user@email.com', 'hash_test', '699999999');
-- Insertar mascota vinculada (verificar ID del usuario insertado)
INSERT INTO `mascotas` (`nombre_mascota`, `tipo_mascota`, `edad`, `descripcion`, `id_usuario`)
VALUES ('Tester', 'Perro', 4, 'Perro de pruebas para DBeaver', 4);
-- Comprobación de relación mediante JOIN
SELECT u.nombre_completo AS Dueno, m.nombre_mascota AS Mascota
FROM usuarios u
JOIN mascotas m ON u.id = m.id_usuario
WHERE u.dni = '99999999T';
-- =============================================================================
-- TEST 2: RESTRICCIONES DE INTEGRIDAD (ERRORES ESPERADOS)
-- =============================================================================
-- Error esperado: DNI duplicado (UK)
INSERT INTO `usuarios` (`nombre_completo`, `dni`, `email`, `password_hash`, `telefono`) 
VALUES ('Otro Usuario', '99999999T', 'otro.email@email.com', 'hash', '600000000');
-- Error esperado: ID de usuario inexistente (FK)
INSERT INTO `mascotas` (`nombre_mascota`, `tipo_mascota`, `edad`, `id_usuario`)
VALUES ('Fantasma', 'Gato', 2, 999);
-- Error esperado: Duplicar validación de la misma cita (UK)
INSERT INTO `historial_citas` (`cita_id`, `doctor_id`, `estado`, `observaciones`) 
VALUES (3, 1, 'asistido', 'Primera validación de testeo');
INSERT INTO `historial_citas` (`cita_id`, `doctor_id`, `estado`, `observaciones`) 
VALUES (3, 1, 'no asistido', 'Intento de duplicar el historial');
-- =============================================================================
-- TEST 3: ELIMINACIÓN EN CASCADA
-- =============================================================================
-- Borrar usuario y verificar propagación en mascotas
DELETE FROM `usuarios` WHERE `dni` = '99999999T';
-- Debe devolver un resultado vacío (0 filas)
SELECT * FROM `mascotas` WHERE `nombre_mascota` = 'Tester';
-- ==============================================================================
-- 4: MAS ERRORES ESPERADOS
-- ==============================================================================
-- Error esperado: Intentar crear un usuario sin DNI (Campo obligatorio)
INSERT INTO usuarios (nombre_completo, email) 
VALUES ('Usuario Incompleto', 'incompleto@email.com');
-- Error esperado: Tipo de dato incorrecto en la edad
INSERT INTO mascotas (nombre_mascota, tipo_mascota, edad, id_usuario)
VALUES ('Mascota Rara', 'Gato', 'TRES AÑOS', 1);
