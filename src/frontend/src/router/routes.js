import {appPermissions} from '@/utils/perms';

// Layouts
import MainLayout from '@/layouts/MainLayout/MainLayout.vue';
import AuthLayout from 'cism-front-base/src/layouts/AuthLayout/AuthLayout.vue';
import NotFoundLayout from 'cism-front-base/src/layouts/NotFoundLayout/NotFoundLayout.vue';

// Views
import MainView from '@/views/MainView/MainView.vue';
import NotFoundView from '@/views/NotFoundView/NotFoundView.vue';
import NotPermView from '@/views/NotPermView/NotPermView.vue';


//user
import AuthView from '@/views/manager_user/AuthView/AuthView.vue';
import UsersIndex from '@/views/manager_user/UsersView/UsersIndex.vue';
import UsersTabView from '@/views/manager_user/UsersView/UsersTabView.vue';
import RolesTabView from '@/views/manager_user/UsersView/RolesTabView.vue';
import UsersCreateView from '@/views/manager_user/UsersView/UsersCreateView.vue';
import UsersUpdateView from '@/views/manager_user/UsersView/UsersUpdateView.vue';
import UsersUpdatePasswordView from '@/views/manager_user/UsersView/UsersUpdatePasswordView.vue';
import RolesCreateView from '@/views/manager_user/UsersView/RolesCreateView.vue';
import RolesUpdateView from '@/views/manager_user/UsersView/RolesUpdateView.vue';

import TaskView from '@/views/TaskView/TaskView.vue';
import TaskPageView from '@/views/TaskView/TaskPageView.vue';
import TaskCreateView from '@/views/TaskView/TaskCreateView.vue';
import TaskUploadFileView from '@/views/TaskView/TaskUploadFileView.vue';
import TaskUpdateView from '@/views/TaskView/TaskUpdateView.vue';


let authRoutes = [
    {
      path: '/auth',
      meta: {title: 'Авторизация'},
      component: AuthLayout,
      children: [{path: '', name: 'auth', component: AuthView}],
    },
  ]
let userRoutes = [
    {
      path: '/users',
      meta: {title: 'Пользователи', perms: appPermissions.CISM_USER_READ_PERMISSION},
      component: MainLayout,
      children: [
        {
          path: '',
          name: 'user-index',
          component: UsersIndex,
          redirect: {name: 'users-tab'},
          children: [
              {path: 'users-tab', name: 'users-tab', component: UsersTabView},
              {path: 'roles-tab', name: 'roles-tab', component: RolesTabView},
          ]
        },
        {path: 'create', name: 'create-user', component: UsersCreateView, meta: {perms: appPermissions.CISM_USER_EDIT_PERMISSION}},
        {path: 'update/:id', name: 'update-user', component: UsersUpdateView, meta: {perms: appPermissions.CISM_USER_EDIT_PERMISSION}},
        {path: 'update-password/:id', name: 'update-user-password', component: UsersUpdatePasswordView, meta: {perms: appPermissions.CISM_USER_EDIT_PERMISSION}},
        {path: 'create-role', name: 'create-role', component: RolesCreateView, meta: {perms: appPermissions.CISM_USER_EDIT_PERMISSION}},
        {path: 'update-role/:id', name: 'update-role', component: RolesUpdateView, meta: {perms: appPermissions.CISM_USER_EDIT_PERMISSION}},
      ],
    },
  ]

let baseRoutes = [
  {
    path: '/dashboard',
    meta: {title: 'Главная'},
    component: MainLayout,
    children: [{path: '', name: 'dashboard', component: MainView, meta: {title: 'Главная', perms: appPermissions.IS_AUTHENTICATED}}],
  },
  {
    path: '/tasks',
    meta: {title: 'Главная', perms: appPermissions.TASK_VIEW_PERMISSION},
    component: MainLayout,
    children: [
      {path: '', name: 'tasks-lists', component: TaskView, meta: {title: 'Задачи', perms: appPermissions.TASK_VIEW_PERMISSION}},
      {path: 'page/:id', name: 'task-page', component: TaskPageView, meta: {perms: appPermissions.TASK_EDIT_PERMISSION}},
      {path: 'create', name: 'create-task', component: TaskCreateView, meta: {perms: appPermissions.TASK_EDIT_PERMISSION}},
      {path: 'upload-file', name: 'upload-file', component: TaskUploadFileView, meta: {perms: appPermissions.TASK_EDIT_PERMISSION}},
      {path: 'update/:id', name: 'update-task', component: TaskUpdateView, meta: {perms: appPermissions.TASK_EDIT_PERMISSION}},
    ],
  },
  {
    path: '/not-group',
    meta: {title: 'Недостаточно прав', isError: true},
    component: NotFoundLayout,
    children: [{path: '', name: 'not-group', component: NotPermView}],
  },
  {
    path: '/:catchAll(.*)',
    meta: {title: '404', isError: true},
    component: NotFoundLayout,
    children: [{path: '', name: 'notfound', component: NotFoundView}],
  },
  {redirect: {name: 'dashboard'},}
];

let routes = [].concat.apply([], [baseRoutes, authRoutes, userRoutes])

export default routes;
