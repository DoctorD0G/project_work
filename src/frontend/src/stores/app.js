import {defineStore} from 'pinia';

export const useAppStore = defineStore('app', {
  state: () => ({
    isVisibleMenu: true,
    appTitle: "Приложение"
  }),
  actions: {
    toggleVisibleMenu() {
      this.isVisibleMenu = !this.isVisibleMenu;
    },
  },
});
