import {appPermissions} from '@/utils/perms';

export const menuList = [
  {
    title: 'Главная',
    icon: 'home',
    link: '/dashboard',
    name: 'dashboard',
  },
  {
    title: 'Пользователи',
    icon: 'group',
    link: '/users',
    name: 'users',
    perms: appPermissions.CISM_USER_READ_PERMISSION
  },
  {
    title: 'Задачи',
    icon: 'home',
    link: '/tasks',
    name: 'tasks-lists',
    perms: appPermissions.TASK_VIEW_PERMISSION
  },
  // Пример реализации пользователей через вложенные элементы меню
  // Можно использовать несколько уровней вложенности, но я бы не рекомендовал больше 3х
  // Потому что выглядит это так себе
  // {
  //   title: 'Настройки',
  //   icon: 'settings',
  //   name: 'settings',
  //   perms: appPermissions.CISM_USER_READ_PERMISSION,
  //   children: [
  //     {
  //       title: 'Пользователи и роли',
  //       icon: 'manage_accounts',
  //       link: '/users/users-tab',
  //       perms: appPermissions.CISM_USER_READ_PERMISSION,
  //       name: 'users_and_roles',
  //     },
  //   ],
  // },
];
