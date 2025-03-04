import {
  LayoutDashboardIcon,BorderAllIcon,
  AlertCircleIcon,
  CircleDotIcon,
  BoxMultiple1Icon,
  LoginIcon, MoodHappyIcon, ApertureIcon, UserPlusIcon
} from 'vue-tabler-icons';

export interface menu {
  header?: string;
  title?: string;
  icon?: any;
  to?: string;
  roles?: string[];  // Ajout du champ 'roles'
  chip?: string;
  BgColor?: string;
  chipBgColor?: string;
  chipColor?: string;
  chipVariant?: string;
  chipIcon?: string;
  children?: menu[];
  disabled?: boolean;
  type?: string;
  subCaption?: string;
}

const sidebarItem: menu[] = [
  { header: 'Home' },
  {
    title: 'Dashboard',
    icon: LayoutDashboardIcon,
    to: '/',
    roles: ['admin', 'user']  // Seuls 'admin' et 'user' y ont accès
  },
  { header: 'ui' },
  {
    title: "Alert",
    icon: AlertCircleIcon,
    to: "/ui-components/alerts",
    roles: ['gestio', 'admin']
  },
  {
    title: "Button",
    icon: CircleDotIcon,
    to: "/ui-components/buttons",
    roles: ['user']
  },
  {
    title: "Cards",
    icon: BoxMultiple1Icon,
    to: "/ui-components/cards",
    roles: ['admin', 'user']
  },
  {
    title: "Tables",
    icon: BorderAllIcon,
    to: "/ui-components/tables",
    roles: ['admin']
  },
  { header: 'Auth' },
  {
    title: 'Login',
    icon: LoginIcon,
    to: '/auth/login',
    roles: ['guest']
  },
  { header: 'Admin' },
  {
    title: 'Register',
    icon: UserPlusIcon,
    to: '/admin/register',
    roles: ['admin']
  },
  {
    title: 'Icons',
    icon: MoodHappyIcon,
    to: '/pages/icons',
    roles: ['admin']
  },
  {
    title: 'Gestion des utilisateurs',
    icon: ApertureIcon,
    to: '/admin/GestionUser',
    roles: ['admin']
  },
];

export default sidebarItem;
