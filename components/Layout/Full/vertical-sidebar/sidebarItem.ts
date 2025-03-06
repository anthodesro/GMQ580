import { 
  IconSettingsCheck,
  IconLayoutDashboard,
  IconAlertCircle,
  IconCircleDot,
  IconBoxMultiple1,
  IconTable,
  IconUserCog,
  IconBuildingBank,
  IconFolderOpen,
  IconFolderCog
} from '@tabler/icons-vue';

export interface menu {
  header?: string;
  title?: string;
  icon?: any;  // Icône est un composant Vue
  to?: string;
  roles?: string[];
}

const sidebarItem: menu[] = [
  { header: 'Home' },
  {
    title: 'Dashboard',
    icon: { component: IconLayoutDashboard },  // ✅ Stocke l'icône sous forme d'objet
    to: '/',
    roles: ['admin', 'user']
  },
  { header: 'UI' },
  {
    title: "Alert",
    icon: { component: IconAlertCircle },
    to: "/ui-components/alerts",
    roles: ['gestio', 'admin']
  },
  {
    title: "Button",
    icon: { component: IconCircleDot },
    to: "/ui-components/buttons",
    roles: ['admin', 'user']
  },
  {
    title: "Cards",
    icon: { component: IconBoxMultiple1 },
    to: "/ui-components/cards",
    roles: ['admin', 'user']
  },
  {
    title: "Tables",
    icon: { component: IconTable },
    to: "/ui-components/tables",
    roles: ['admin']
  },

  { header: 'Projets' },
  {
    title: 'Mes Projets',
    icon: { component: IconFolderOpen },
    to: '/projet',
    roles: ['guest']
  },
  {
    title: 'Mes Projets',
    icon: { component: IconFolderCog },
    to: '/projets',
    roles: ['admin', 'gestio']
  },
  {
    title: 'Configuration',
    icon: { component: IconFolderCog },
    to: '/projets/config',
    roles: ['admin', 'gestio']
  },

  { header: 'Trésorerie' },
  {
    title: 'Banque',
    icon: { component: IconBuildingBank },
    to: '/tresorerie',
    roles: ['guest', 'admin', 'gestio']
  },

  { header: 'Admin' },
  {
    title: 'Utilisateurs',
    icon: { component: IconUserCog },
    to: '/admin/GestionUser',
    roles: ['admin']
  },
  {
    title: 'Configurations',
    icon: { component: IconSettingsCheck },
    to: '/admin/config',
    roles: ['admin']
  },
];

export default sidebarItem;
