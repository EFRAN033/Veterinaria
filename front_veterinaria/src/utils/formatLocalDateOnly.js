/**
 * Fecha calendario en zona local (YYYY-MM-DD).
 * Evita el desfase de toISOString() (UTC) al agendar citas.
 */
export function formatLocalDateOnly(value) {
  if (!value) return '';
  const d = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(d.getTime())) return '';
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}
