// Reutilizable: variant → CSS class, type="button" por defecto, reenvía props.
export default function Button({ variant = "primary", children, ...rest }) {
  return <button className={`btn btn-${variant}`} type="button" {...rest}>{children}</button>;
}
