/**
 * EmptyState - Reusable empty state component with icon, message, and action
 */
import PropTypes from 'prop-types';

export default function EmptyState({
  icon,
  title,
  message,
  action,
  children
}) {
  return (
    <div className="text-center py-12">
      {icon && (
        <div className="mx-auto h-24 w-24 flex items-center justify-center rounded-full bg-gray-100 mb-4">
          <span className="text-5xl">{icon}</span>
        </div>
      )}
      <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
      {message && (
        <p className="text-sm text-gray-600 max-w-md mx-auto mb-6">{message}</p>
      )}
      {action && (
        <button
          onClick={action.onClick}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          {action.icon && <span className="mr-2">{action.icon}</span>}
          {action.label}
        </button>
      )}
      {children}
    </div>
  );
}

EmptyState.propTypes = {
  icon: PropTypes.string,
  title: PropTypes.string.isRequired,
  message: PropTypes.string,
  action: PropTypes.shape({
    label: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
    icon: PropTypes.node,
  }),
  children: PropTypes.node,
};
