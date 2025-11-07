/**
 * Main layout component with navigation
 */
import { Fragment } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Menu, Transition } from '@headlessui/react';
import {
  Bars3Icon,
  BookOpenIcon,
  DocumentTextIcon,
  AcademicCapIcon,
  Cog6ToothIcon,
  UserCircleIcon,
  ArrowRightOnRectangleIcon,
  SparklesIcon,
  QueueListIcon,
  CodeBracketIcon,
} from '@heroicons/react/24/outline';
import useAuthStore from '../store/authStore';

export default function Layout({ children }) {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const navigation = [
    { name: 'Dashboard', href: '/', icon: AcademicCapIcon, roles: ['all'] },
    {
      name: 'Knowledge Base',
      href: '/knowledge',
      icon: BookOpenIcon,
      roles: ['all'],
    },
    {
      name: 'Content',
      href: '/content',
      icon: DocumentTextIcon,
      roles: ['author', 'editor', 'knowledge_engineer'],
    },
    {
      name: 'Agents',
      href: '/agents',
      icon: SparklesIcon,
      roles: ['author', 'editor', 'knowledge_engineer'],
    },
    {
      name: 'Workflows',
      href: '/workflows',
      icon: QueueListIcon,
      roles: ['author', 'editor', 'knowledge_engineer'],
    },
    {
      name: 'Skills',
      href: '/skills',
      icon: CodeBracketIcon,
      roles: ['author', 'editor', 'knowledge_engineer'],
    },
    {
      name: 'Reviews',
      href: '/reviews',
      icon: Bars3Icon,
      roles: ['editor', 'knowledge_engineer'],
    },
    {
      name: 'Configs',
      href: '/configs',
      icon: Cog6ToothIcon,
      roles: ['knowledge_engineer'],
    },
  ];

  const canAccessRoute = (route) => {
    if (route.roles.includes('all')) return true;
    return route.roles.includes(user?.role);
  };

  const isActive = (path) => {
    return location.pathname === path ||
      (path !== '/' && location.pathname.startsWith(path));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              {/* Logo */}
              <div className="flex-shrink-0 flex items-center">
                <Link to="/" className="flex items-center">
                  <BookOpenIcon className="h-8 w-8 text-primary-600" />
                  <span className="ml-2 text-xl font-bold text-gray-900">
                    Nova
                  </span>
                </Link>
              </div>

              {/* Navigation Links */}
              <div className="hidden sm:ml-6 sm:flex sm:space-x-4">
                {navigation
                  .filter((item) => canAccessRoute(item))
                  .map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`inline-flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                        isActive(item.href)
                          ? 'bg-primary-50 text-primary-700 border-b-2 border-primary-700'
                          : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <item.icon className="h-5 w-5 mr-2" />
                      {item.name}
                    </Link>
                  ))}
              </div>
            </div>

            {/* User Menu */}
            <div className="flex items-center">
              <Menu as="div" className="relative ml-3">
                <Menu.Button className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-primary-500">
                  <UserCircleIcon className="h-8 w-8 text-gray-400" />
                  <span className="ml-2 text-gray-700">{user?.full_name || user?.email}</span>
                </Menu.Button>

                <Transition
                  as={Fragment}
                  enter="transition ease-out duration-100"
                  enterFrom="transform opacity-0 scale-95"
                  enterTo="transform opacity-100 scale-100"
                  leave="transition ease-in duration-75"
                  leaveFrom="transform opacity-100 scale-100"
                  leaveTo="transform opacity-0 scale-95"
                >
                  <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div className="px-4 py-2 text-xs text-gray-500 border-b">
                      Role: <span className="font-medium">{user?.role}</span>
                    </div>
                    <Menu.Item>
                      {({ active }) => (
                        <Link
                          to="/profile"
                          className={`${
                            active ? 'bg-gray-100' : ''
                          } block px-4 py-2 text-sm text-gray-700`}
                        >
                          Your Profile
                        </Link>
                      )}
                    </Menu.Item>
                    <Menu.Item>
                      {({ active }) => (
                        <button
                          onClick={handleLogout}
                          className={`${
                            active ? 'bg-gray-100' : ''
                          } w-full text-left px-4 py-2 text-sm text-gray-700 flex items-center`}
                        >
                          <ArrowRightOnRectangleIcon className="h-4 w-4 mr-2" />
                          Sign out
                        </button>
                      )}
                    </Menu.Item>
                  </Menu.Items>
                </Transition>
              </Menu>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}
