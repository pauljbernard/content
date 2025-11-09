/**
 * Main layout component with navigation
 */
import { Fragment, useState } from 'react';
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
  ArrowDownTrayIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ServerIcon,
  CubeIcon,
  RectangleStackIcon,
  CircleStackIcon,
  KeyIcon,
} from '@heroicons/react/24/outline';
import useAuthStore from '../store/authStore';

export default function Layout({ children }) {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  // Navigation organized into sections
  const navigationSections = [
    {
      name: 'Main',
      items: [
        { name: 'Dashboard', href: '/', icon: AcademicCapIcon, roles: ['all'] },
        { name: 'Knowledge Base', href: '/knowledge', icon: BookOpenIcon, roles: ['all'] },
        { name: 'Import', href: '/importers', icon: ArrowDownTrayIcon, roles: ['author', 'editor', 'knowledge_engineer'] },
        { name: 'Content', href: '/content', icon: DocumentTextIcon, roles: ['author', 'editor', 'knowledge_engineer'] },
        { name: 'Queues', href: '/queues', icon: QueueListIcon, roles: ['author', 'editor', 'knowledge_engineer'] },
      ],
    },
    {
      name: 'Taxonomy',
      items: [
        { name: 'Content Types', href: '/content-types', icon: CubeIcon, roles: ['editor', 'knowledge_engineer'] },
        { name: 'Core Setup', href: '/content-types/setup', icon: Cog6ToothIcon, roles: ['knowledge_engineer'] },
        { name: 'Templates', href: '/content-types/templates', icon: RectangleStackIcon, roles: ['editor', 'knowledge_engineer'] },
      ],
    },
    {
      name: 'Automation',
      items: [
        { name: 'Agents', href: '/agents', icon: SparklesIcon, roles: ['author', 'editor', 'knowledge_engineer'] },
        { name: 'Workflows', href: '/workflows', icon: QueueListIcon, roles: ['author', 'editor', 'knowledge_engineer'] },
        { name: 'Skills', href: '/skills', icon: CodeBracketIcon, roles: ['author', 'editor', 'knowledge_engineer'] },
      ],
    },
    {
      name: 'System',
      items: [
        { name: 'Your Profile', href: '/profile', icon: UserCircleIcon, roles: ['all'] },
        { name: 'Indexing', href: '/indexing', icon: ServerIcon, roles: ['knowledge_engineer'] },
        { name: 'Secrets', href: '/secrets', icon: KeyIcon, roles: ['knowledge_engineer'] },
        { name: 'Database Settings', href: '/settings/database', icon: CircleStackIcon, roles: ['knowledge_engineer'] },
        { name: 'LLM Settings', href: '/settings/llm', icon: SparklesIcon, roles: ['knowledge_engineer'] },
      ],
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
    <div className="min-h-screen bg-gray-50 flex">
      {/* Left Sidebar */}
      <aside
        className={`bg-white border-r border-gray-200 flex flex-col transition-all duration-300 ${
          sidebarCollapsed ? 'w-16' : 'w-64'
        }`}
      >
        {/* Sidebar Header - Empty space to match top bar height */}
        <div className="h-16 border-b border-gray-200"></div>

        {/* Navigation Sections */}
        <nav className="flex-1 overflow-y-auto py-4">
          {navigationSections.map((section, sectionIdx) => (
            <div key={section.name} className={sectionIdx > 0 ? 'mt-8' : ''}>
              {!sidebarCollapsed && (
                <div className="px-4 mb-2">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    {section.name}
                  </h3>
                </div>
              )}
              <div className="space-y-1 px-2">
                {section.items
                  .filter((item) => canAccessRoute(item))
                  .map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                        isActive(item.href)
                          ? 'bg-primary-50 text-primary-700'
                          : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                      title={sidebarCollapsed ? item.name : ''}
                    >
                      <item.icon className="h-5 w-5 flex-shrink-0" />
                      {!sidebarCollapsed && <span className="ml-3">{item.name}</span>}
                    </Link>
                  ))}
              </div>
            </div>
          ))}
        </nav>

        {/* Collapse Toggle Button */}
        <div className="border-t border-gray-200 p-4">
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="flex items-center justify-center w-full px-3 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-50 hover:text-gray-900"
            title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {sidebarCollapsed ? (
              <ChevronRightIcon className="h-5 w-5" />
            ) : (
              <>
                <ChevronLeftIcon className="h-5 w-5" />
                <span className="ml-2">Collapse</span>
              </>
            )}
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Navigation Bar */}
        <nav className="bg-white shadow-sm border-b border-gray-200 h-16">
          <div className="h-full px-4 sm:px-6 lg:px-8 flex items-center justify-between">
            {/* Logo on the left */}
            <Link to="/" className="flex items-center">
              <BookOpenIcon className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">Nova</span>
            </Link>

            {/* User Menu on the right */}
            <div className="flex items-center">
              <Menu as="div" className="relative">
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
        </nav>

        {/* Page Content */}
        <main className="flex-1 overflow-auto">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
