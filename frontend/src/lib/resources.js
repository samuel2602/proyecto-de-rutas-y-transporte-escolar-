export const resources = {
  roles: { label: 'Roles', icon: '◈', fields: [['nombre', 'Nombre', 'text', true], ['descripcion', 'Descripción', 'text']] },
  usuarios: { label: 'Usuarios', icon: '◎', fields: [['nombre', 'Nombres', 'text', true], ['apellido', 'Apellidos', 'text', true], ['correo', 'Correo', 'email', true], ['telefono', 'Teléfono', 'tel'], ['rol_id', 'ID de rol', 'number', true]] },
  acudientes: { label: 'Acudientes', icon: '♧', fields: [['nombre', 'Nombres', 'text', true], ['apellido', 'Apellidos', 'text', true], ['documento', 'Documento', 'text', true], ['telefono', 'Teléfono', 'tel', true], ['correo', 'Correo', 'email'], ['usuario_id', 'ID de usuario', 'number', true]] },
  estudiantes: { label: 'Estudiantes', icon: '♙', fields: [['nombre', 'Nombres', 'text', true], ['apellido', 'Apellidos', 'text', true], ['documento', 'Documento', 'text', true], ['grado', 'Grado', 'text'], ['direccion', 'Dirección', 'text'], ['acudiente_id', 'ID de acudiente', 'number', true]] },
  conductores: { label: 'Conductores', icon: '◉', fields: [['nombre', 'Nombres', 'text', true], ['apellido', 'Apellidos', 'text', true], ['documento', 'Documento', 'text', true], ['licencia', 'Licencia', 'text', true], ['telefono', 'Teléfono', 'tel'], ['activo', 'Activo', 'select', false, ['true', 'false']]] },
  vehiculos: { label: 'Vehículos', icon: '▣', fields: [['placa', 'Placa', 'text', true], ['marca', 'Marca', 'text'], ['modelo', 'Modelo', 'text'], ['capacidad', 'Capacidad', 'number', true], ['estado', 'Estado', 'select', false, ['Disponible', 'En ruta', 'Mantenimiento']]] },
  rutas: { label: 'Rutas', icon: '⌁', fields: [['nombre', 'Nombre de la ruta', 'text', true], ['descripcion', 'Descripción', 'text'], ['hora_salida', 'Hora de salida', 'time', true], ['hora_llegada', 'Hora de llegada', 'time'], ['conductor_id', 'ID de conductor', 'number', true], ['vehiculo_id', 'ID de vehículo', 'number', true], ['estado', 'Estado', 'select', false, ['Activa', 'Inactiva']]] },
  paraderos: { label: 'Paraderos', icon: '⌖', fields: [['nombre', 'Nombre', 'text', true], ['direccion', 'Dirección', 'text', true], ['referencia', 'Referencia', 'text'], ['latitud', 'Latitud', 'number'], ['longitud', 'Longitud', 'number']] },
  'estudiante-ruta': { label: 'Asignaciones', icon: '↔', fields: [['estudiante_id', 'ID de estudiante', 'number', true], ['ruta_id', 'ID de ruta', 'number', true], ['paradero_id', 'ID de paradero', 'number', true]] },
  'registros-abordaje': { label: 'Abordajes', icon: '✓', fields: [['estudiante_id', 'ID de estudiante', 'number', true], ['ruta_id', 'ID de ruta', 'number', true], ['tipo', 'Tipo', 'select', true, ['Subida', 'Bajada']]] },
};

export const roleAccess = {
  Administrador: Object.keys(resources),
  Conductor: ['rutas', 'estudiantes', 'registros-abordaje'],
  Acudiente: ['rutas', 'paraderos'],
  Estudiante: ['rutas', 'paraderos'],
};
