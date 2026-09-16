<script>
  import { onMount } from 'svelte';
  import { api } from './lib/api.js';
  import { resources, roleAccess } from './lib/resources.js';

  const demoAccounts = [
    { username: 'admin', password: '1234', role: 'Administrador', name: 'Administrador' },
    { username: 'conductor', password: '2026**', role: 'Conductor', name: 'Conductor' },
    { username: 'acudiente', password: '2026**', role: 'Acudiente', name: 'Acudiente' },
    { username: 'estudiante', password: '2026**', role: 'Estudiante', name: 'Estudiante' },
  ];

  let session = null;
  let username = '';
  let password = '';
  let loginError = '';
  let active = 'inicio';
  let records = [];
  let loading = false;
  let error = '';
  let notice = '';
  let showForm = false;
  let form = {};
  let editingId = null;

  $: config = resources[active];
  $: allowedResources = session ? roleAccess[session.role] : [];
  $: columns = config?.fields?.slice(0, 4) ?? [];
  $: isAdmin = session?.role === 'Administrador';
  $: canCreate = isAdmin || (session?.role === 'Conductor' && active === 'registros-abordaje');
  $: welcome = session?.role === 'Administrador'
    ? ['Administración completa', 'Controla toda la operación de transporte escolar.', 'rutas']
    : session?.role === 'Conductor'
      ? ['Tu jornada de ruta', 'Consulta los estudiantes asignados y registra abordajes.', 'registros-abordaje']
      : session?.role === 'Acudiente'
        ? ['Información de transporte', 'Consulta las rutas y paraderos disponibles para tu familia.', 'rutas']
        : ['Tu transporte escolar', 'Consulta la ruta y los paraderos de tu recorrido.', 'rutas'];

  function login() {
    const account = demoAccounts.find((item) => item.username === username.trim().toLowerCase() && item.password === password);
    if (!account) { loginError = 'Usuario o contraseña incorrectos.'; return; }
    session = account;
    localStorage.setItem('rutaEscolarSession', JSON.stringify(account));
    active = 'inicio'; loginError = ''; password = '';
  }

  function logout() {
    localStorage.removeItem('rutaEscolarSession');
    session = null; active = 'inicio'; records = []; showForm = false;
  }

  async function load(resource = active) {
    if (!resources[resource] || !allowedResources.includes(resource)) return;
    loading = true; error = '';
    try { records = await api.list(resource); }
    catch (err) { error = err.message; records = []; }
    finally { loading = false; }
  }

  function select(resource) {
    if (!allowedResources.includes(resource)) return;
    active = resource; records = []; notice = ''; error = ''; showForm = false; load(resource);
  }

  function openForm(record = null) {
    editingId = record?.id ?? null;
    form = Object.fromEntries(config.fields.map(([key]) => [key, record?.[key] ?? '']));
    showForm = true; error = '';
  }

  function normalize() {
    const data = { ...form };
    for (const [key, , type] of config.fields) {
      if (data[key] === '') { delete data[key]; continue; }
      if (type === 'number') data[key] = Number(data[key]);
      if (key === 'activo') data[key] = data[key] === 'true';
    }
    return data;
  }

  async function save() {
    error = ''; notice = '';
    try {
      if (editingId) await api.update(active, editingId, normalize());
      else await api.create(active, normalize());
      showForm = false; notice = editingId ? 'Registro actualizado correctamente.' : 'Registro creado correctamente.'; load();
    }
    catch (err) { error = err.message; }
  }

  async function remove(id) {
    if (!isAdmin || !confirm('¿Eliminar este registro? Esta acción no se puede deshacer.')) return;
    try { await api.remove(active, id); notice = 'Registro eliminado correctamente.'; load(); }
    catch (err) { error = err.message; }
  }

  function display(value) { return value === true ? 'Sí' : value === false ? 'No' : value ?? '—'; }

  onMount(() => {
    try { session = JSON.parse(localStorage.getItem('rutaEscolarSession')) || null; } catch { localStorage.removeItem('rutaEscolarSession'); }
  });
</script>

<svelte:head><title>RutaEscolar</title><meta name="description" content="Gestión de transporte escolar" /></svelte:head>

{#if !session}
  <main class="login-page"><section class="login-brand"><span class="brand-mark">R</span><div><p class="eyebrow">RUTAESCOLAR</p><h1>La operación escolar, en movimiento.</h1><p>Un acceso pensado para cada persona que hace posible el recorrido.</p></div><div class="login-decoration">⌁</div></section>
  <section class="login-card"><div><p class="eyebrow">BIENVENIDO</p><h2>Inicia sesión</h2><p class="muted">Usa las credenciales asignadas a tu perfil.</p></div><form on:submit|preventDefault={login}><label>Usuario<input bind:value={username} autocomplete="username" placeholder="Tu usuario" /></label><label>Contraseña<input bind:value={password} type="password" autocomplete="current-password" placeholder="Tu contraseña" /></label>{#if loginError}<p class="error">{loginError}</p>{/if}<button class="primary wide" type="submit">Ingresar</button></form><p class="demo-note">Acceso de demostración para los cuatro perfiles.</p></section></main>
{:else}
  <div class="shell">
    <aside class="sidebar"><div class="brand"><span class="brand-mark">R</span><div><strong>RutaEscolar</strong><small>{session.role}</small></div></div><nav aria-label="Navegación principal"><button class:active={active === 'inicio'} on:click={() => { active = 'inicio'; showForm = false; }}><span>▦</span> Inicio</button><p>{isAdmin ? 'ADMINISTRACIÓN' : 'MI TRANSPORTE'}</p>{#each allowedResources as key}<button class:active={active === key} on:click={() => select(key)}><span>{resources[key].icon}</span> {resources[key].label}</button>{/each}</nav><div class="sidebar-footer"><span class="avatar">{session.name.slice(0, 2).toUpperCase()}</span><div><strong>{session.name}</strong><small>{session.role}</small></div><button class="logout" on:click={logout} title="Cerrar sesión">↪</button></div></aside>
    <main><header><div><p class="eyebrow">{session.role.toUpperCase()}</p><h1>{active === 'inicio' ? `Hola, ${session.name}` : config.label}</h1></div><span class="date">{new Intl.DateTimeFormat('es-CO', { dateStyle: 'full' }).format(new Date())}</span></header>
      {#if active === 'inicio'}
        <section class="welcome"><div><span class="pill">{session.role.toUpperCase()}</span><h2>{welcome[0]}</h2><p>{welcome[1]}</p><button class="primary" on:click={() => select(welcome[2])}>Continuar <span>→</span></button></div><div class="route-mark">⌁</div></section>
        <section class="role-guidance"><h2>{isAdmin ? 'Administración del sistema' : 'Tu espacio de trabajo'}</h2>{#if isAdmin}<p>Gestiona las 10 tablas: usuarios, roles, familias, operación y registros.</p>{:else if session.role === 'Conductor'}<p>Consulta tus rutas y estudiantes. Registra la subida o bajada de cada estudiante desde Abordajes.</p>{:else if session.role === 'Acudiente'}<p>Consulta los recorridos y paraderos para planificar el transporte de tu familia.</p>{:else}<p>Consulta la ruta y los puntos de encuentro de tu transporte escolar.</p>{/if}<div class="access-chips">{#each allowedResources as key}<button on:click={() => select(key)}>{resources[key].icon} {resources[key].label}</button>{/each}</div></section>
      {:else}
        <section class="content-header"><p>{isAdmin ? `${records.length} registros en total` : 'Consulta de información de transporte'}</p>{#if canCreate}<button class="primary" on:click={openForm}>＋ Añadir</button>{/if}</section>{#if notice}<div class="notice">✓ {notice}</div>{/if}{#if error}<div class="error">{error}</div>{/if}
        <section class="panel"><div class="panel-top"><strong>{config.label}</strong><button class="refresh" on:click={() => load()}>↻ Actualizar</button></div>{#if loading}<div class="empty">Cargando información…</div>{:else if records.length === 0}<div class="empty"><span>◌</span><strong>No hay registros disponibles</strong><p>{isAdmin ? 'Agrega el primer registro para empezar.' : 'No hay información asignada para mostrar.'}</p></div>{:else}<div class="table-wrap"><table><thead><tr><th>ID</th>{#each columns as [, label]}<th>{label}</th>{/each}{#if isAdmin}<th></th>{/if}</tr></thead><tbody>{#each records as record}<tr><td>#{record.id}</td>{#each columns as [key]}<td>{display(record[key])}</td>{/each}{#if isAdmin}<td><button class="edit" on:click={() => openForm(record)}>Editar</button><button class="delete" on:click={() => remove(record.id)}>Eliminar</button></td>{/if}</tr>{/each}</tbody></table></div>{/if}</section>
      {/if}
    </main>
    {#if showForm}<div class="backdrop" role="presentation" on:click={() => showForm = false}></div><div class="modal" aria-modal="true" role="dialog" aria-labelledby="form-title"><div class="modal-title"><div><p class="eyebrow">{editingId ? 'EDITAR REGISTRO' : 'NUEVO REGISTRO'}</p><h2 id="form-title">{editingId ? 'Editar' : 'Añadir'} {config.label}</h2></div><button class="close" on:click={() => showForm = false}>×</button></div><form on:submit|preventDefault={save}>{#each config.fields as [key, label, type, required, options]}<label>{label}{#if required}<b>*</b>{/if}{#if type === 'select'}<select required={required} bind:value={form[key]}><option value="">Selecciona una opción</option>{#each options as option}<option value={option}>{option}</option>{/each}</select>{:else}<input required={required} type={type} bind:value={form[key]} />{/if}</label>{/each}<div class="form-actions"><button type="button" class="secondary" on:click={() => showForm = false}>Cancelar</button><button class="primary" type="submit">Guardar</button></div></form></div>{/if}
  </div>
{/if}
