import { defineNuxtRouteMiddleware } from 'nuxt3';
import sqlite3 from 'sqlite3';

// Remplacer par vos informations de connexion à la base de données
const DB_PATH = 'path_to_your_database.db'; // Remplacez par le chemin réel vers votre base .db
const db = new sqlite3.Database(DB_PATH);

// Middleware pour charger les données à partir de la base de données
export default defineNuxtRouteMiddleware(async (to, from) => {
  if (process.server) return; // Empêche l'exécution côté serveur, sessionStorage n'est pas disponible

  const token = sessionStorage.getItem('token') || localStorage.getItem('token');
  const userRole = sessionStorage.getItem('role') || localStorage.getItem('role');

  if (!token || !userRole) {
    return navigateTo('/auth/login');
  }

  // Exemple de lecture des transactions récentes
  const recentTransaction = await new Promise<any[]>((resolve, reject) => {
    db.all('SELECT * FROM recent_transactions ORDER BY time DESC LIMIT 6', [], (err, rows) => {
      if (err) {
        reject(err);
        return;
      }
      resolve(rows.map(row => ({
        title: row.time,
        subtitle: row.description,
        textcolor: row.textcolor,
        boldtext: row.boldtext === 1, // Supposons que 1 = true et 0 = false
        line: row.line === 1,
        link: row.link || '',
        url: row.url || ''
      })));
    });
  });

  // Exemple de lecture des performances produits
  const productPerformance = await new Promise<any[]>((resolve, reject) => {
    db.all('SELECT * FROM product_performance', [], (err, rows) => {
      if (err) {
        reject(err);
        return;
      }
      resolve(rows.map(row => ({
        id: row.id,
        name: row.name,
        post: row.post,
        pname: row.pname,
        status: row.status,
        statuscolor: row.statuscolor,
        budget: row.budget
      })));
    });
  });

  // Exemple de lecture des cartes de produits
  const productsCard = await new Promise<any[]>((resolve, reject) => {
    db.all('SELECT * FROM products_card', [], (err, rows) => {
      if (err) {
        reject(err);
        return;
      }
      resolve(rows.map(row => ({
        title: row.title,
        link: row.link,
        photo: row.photo, // Assurez-vous que le chemin est correct pour vos images
        salesPrice: row.salesPrice,
        price: row.price,
        rating: row.rating
      })));
    });
  });

  // Vous pouvez maintenant utiliser `recentTransaction`, `productPerformance`, `productsCard` comme vous le feriez normalement.
  return { recentTransaction, productPerformance, productsCard };
});
