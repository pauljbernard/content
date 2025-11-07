/**
 * Toast notification utilities
 */
import toast from 'react-hot-toast';

// Success toast
export const showSuccess = (message) => {
  toast.success(message, {
    duration: 3000,
    position: 'top-right',
    style: {
      background: '#10B981',
      color: '#fff',
    },
  });
};

// Error toast
export const showError = (message, error = null) => {
  const errorMessage = error?.response?.data?.detail || error?.message || message;

  toast.error(errorMessage, {
    duration: 5000,
    position: 'top-right',
    style: {
      background: '#EF4444',
      color: '#fff',
    },
  });
};

// Warning toast
export const showWarning = (message) => {
  toast(message, {
    duration: 4000,
    position: 'top-right',
    icon: '⚠️',
    style: {
      background: '#F59E0B',
      color: '#fff',
    },
  });
};

// Info toast
export const showInfo = (message) => {
  toast(message, {
    duration: 3000,
    position: 'top-right',
    icon: 'ℹ️',
    style: {
      background: '#3B82F6',
      color: '#fff',
    },
  });
};

// Loading toast (returns toast id for dismissal)
export const showLoading = (message) => {
  return toast.loading(message, {
    position: 'top-right',
  });
};

// Dismiss a specific toast
export const dismissToast = (toastId) => {
  toast.dismiss(toastId);
};

// Promise toast (automatically shows loading, success, or error)
export const showPromise = (promise, messages) => {
  return toast.promise(
    promise,
    {
      loading: messages.loading || 'Loading...',
      success: messages.success || 'Success!',
      error: (err) => messages.error || err?.response?.data?.detail || err?.message || 'Something went wrong',
    },
    {
      position: 'top-right',
    }
  );
};
