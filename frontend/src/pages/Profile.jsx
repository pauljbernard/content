/**
 * Profile page - user profile management with multi-tenant support
 */
import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  UserCircleIcon,
  CheckIcon,
  BuildingOfficeIcon,
  GlobeAltIcon,
  ShieldCheckIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';
import useAuthStore from '../store/authStore';
import api from '../services/api';
import Layout from '../components/Layout';

export default function Profile() {
  const { user, updateUser } = useAuthStore();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    confirmPassword: '',
    locale: 'en-US',
    grades: [],
    subjects: [],
  });
  const [success, setSuccess] = useState(false);

  // Fetch profile data from new endpoint
  const { data: profileData, isLoading: profileLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const response = await api.get('/profile');
      return response.data;
    },
    enabled: !!user,
  });

  // Fetch tenant info
  const { data: tenantData } = useQuery({
    queryKey: ['profile-tenant'],
    queryFn: async () => {
      const response = await api.get('/profile/tenant');
      return response.data;
    },
    enabled: !!user,
  });

  // Update form data when profile loads
  useEffect(() => {
    if (profileData) {
      const attrs = profileData.profile?.attrs || {};
      setFormData({
        full_name: attrs.full_name || '',
        email: profileData.account?.email || '',
        password: '',
        confirmPassword: '',
        locale: profileData.account?.locale || 'en-US',
        grades: profileData.profile?.grades || [],
        subjects: profileData.profile?.subjects || [],
      });
    }
  }, [profileData]);

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: async (data) => {
      const response = await api.put('/profile', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['profile']);
      queryClient.invalidateQueries(['profile-tenant']);
      setSuccess(true);
      setFormData(prev => ({ ...prev, password: '', confirmPassword: '' }));
      setTimeout(() => setSuccess(false), 3000);
    },
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleMultiSelectChange = (name, value) => {
    setFormData((prev) => {
      const currentValues = prev[name] || [];
      if (currentValues.includes(value)) {
        return { ...prev, [name]: currentValues.filter(v => v !== value) };
      } else {
        return { ...prev, [name]: [...currentValues, value] };
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccess(false);

    if (formData.password && formData.password !== formData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    const updateData = {
      full_name: formData.full_name,
      locale: formData.locale,
      grades: formData.grades,
      subjects: formData.subjects,
    };

    // Only include password if changed
    if (formData.password) {
      // Also update via legacy endpoint for password
      await updateUser({ password: formData.password });
    }

    updateProfileMutation.mutate(updateData);
  };

  if (profileLoading) {
    return (
      <Layout>
        <div className="max-w-4xl mx-auto">
          <div className="animate-pulse space-y-4">
            <div className="h-12 bg-gray-200 rounded w-1/3"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </div>
      </Layout>
    );
  }

  const gradeOptions = ['K', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'];
  const subjectOptions = ['Math', 'ELA', 'Science', 'Social Studies'];
  const localeOptions = [
    { value: 'en-US', label: 'English (US)' },
    { value: 'es-MX', label: 'Spanish (Mexico)' },
    { value: 'fr-FR', label: 'French (France)' },
    { value: 'de-DE', label: 'German (Germany)' },
  ];

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <UserCircleIcon className="h-12 w-12 text-gray-400 mr-4" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Profile Settings</h1>
              <p className="mt-1 text-sm text-gray-500">
                Manage your account information and preferences
              </p>
            </div>
          </div>

          {/* Tenant/Org Badge */}
          {tenantData && (
            <div className="text-right">
              <div className="flex items-center text-sm text-gray-500">
                <BuildingOfficeIcon className="h-4 w-4 mr-1" />
                <span>{tenantData.org_name}</span>
              </div>
              <div className="flex items-center text-xs text-gray-400">
                <GlobeAltIcon className="h-3 w-3 mr-1" />
                <span>{tenantData.tenant_name}</span>
              </div>
            </div>
          )}
        </div>

        {/* Tenant & Organization Info */}
        {tenantData && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start">
              <BuildingOfficeIcon className="h-6 w-6 text-blue-600 mr-3 mt-0.5" />
              <div className="flex-1">
                <h3 className="text-sm font-medium text-blue-900">Organization Context</h3>
                <div className="mt-2 grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-blue-700 font-medium">Tenant:</span>
                    <span className="ml-2 text-blue-900">{tenantData.tenant_name}</span>
                    <span className="ml-2 text-xs text-blue-600">({tenantData.tenant_plan})</span>
                  </div>
                  <div>
                    <span className="text-blue-700 font-medium">Organization:</span>
                    <span className="ml-2 text-blue-900">{tenantData.org_name}</span>
                    {tenantData.org_type && (
                      <span className="ml-2 text-xs text-blue-600">({tenantData.org_type})</span>
                    )}
                  </div>
                </div>
                {tenantData.is_superuser && (
                  <div className="mt-2 flex items-center text-xs text-blue-800">
                    <ShieldCheckIcon className="h-4 w-4 mr-1" />
                    <span className="font-medium">Super User</span>
                    <span className="ml-2">- Cross-tenant access enabled</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Profile Form */}
        <form onSubmit={handleSubmit} className="bg-white shadow rounded-lg p-6">
          <div className="space-y-6">
            {/* User Info */}
            <div className="pb-6 border-b">
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Account Information
              </h2>

              <div className="grid grid-cols-2 gap-4">
                {/* Full Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                {/* Email (Read-only) */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    disabled
                    className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                  />
                </div>

                {/* Role (Read-only) */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Role
                  </label>
                  <input
                    type="text"
                    value={profileData?.profile?.role || user?.role || ''}
                    disabled
                    className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Contact an administrator to change your role
                  </p>
                </div>

                {/* Locale */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Language
                  </label>
                  <select
                    name="locale"
                    value={formData.locale}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    {localeOptions.map(opt => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Teaching Context (for teachers/authors) */}
            {(profileData?.profile?.role === 'teacher' || profileData?.profile?.role === 'content_author') && (
              <div className="pb-6 border-b">
                <div className="flex items-center mb-4">
                  <AcademicCapIcon className="h-5 w-5 text-gray-400 mr-2" />
                  <h2 className="text-lg font-medium text-gray-900">
                    Teaching Context
                  </h2>
                </div>

                <div className="space-y-4">
                  {/* Grade Levels */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Grade Levels
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {gradeOptions.map(grade => (
                        <button
                          key={grade}
                          type="button"
                          onClick={() => handleMultiSelectChange('grades', grade)}
                          className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                            formData.grades.includes(grade)
                              ? 'bg-primary-600 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {grade}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Subjects */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Subject Areas
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {subjectOptions.map(subject => (
                        <button
                          key={subject}
                          type="button"
                          onClick={() => handleMultiSelectChange('subjects', subject)}
                          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                            formData.subjects.includes(subject)
                              ? 'bg-primary-600 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {subject}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Change Password */}
            <div className="pb-6 border-b">
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Change Password
              </h2>
              <p className="text-sm text-gray-500 mb-4">
                Leave blank to keep your current password
              </p>

              <div className="grid grid-cols-2 gap-4">
                {/* New Password */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    New Password
                  </label>
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Enter new password"
                  />
                </div>

                {/* Confirm Password */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm New Password
                  </label>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Confirm new password"
                  />
                </div>
              </div>
            </div>

            {/* Account Stats */}
            <div>
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Account Activity
              </h2>
              <div className="grid grid-cols-3 gap-4">
                <div className="p-4 bg-gray-50 rounded-md">
                  <p className="text-sm text-gray-500">Member Since</p>
                  <p className="mt-1 text-lg font-medium text-gray-900">
                    {user?.created_at
                      ? new Date(user.created_at).toLocaleDateString()
                      : 'N/A'}
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-md">
                  <p className="text-sm text-gray-500">Last Login</p>
                  <p className="mt-1 text-lg font-medium text-gray-900">
                    {user?.last_login
                      ? new Date(user.last_login).toLocaleDateString()
                      : 'Never'}
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-md">
                  <p className="text-sm text-gray-500">Account Status</p>
                  <p className="mt-1 text-lg font-medium text-gray-900">
                    {profileData?.account?.status || 'Active'}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Success Message */}
          {success && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md flex items-center">
              <CheckIcon className="h-5 w-5 text-green-600 mr-2" />
              <span className="text-sm text-green-800">
                Profile updated successfully!
              </span>
            </div>
          )}

          {/* Actions */}
          <div className="mt-6 flex justify-end">
            <button
              type="submit"
              disabled={updateProfileMutation.isPending}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50"
            >
              {updateProfileMutation.isPending ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
