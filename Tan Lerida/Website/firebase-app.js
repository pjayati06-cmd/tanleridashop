// Firebase configuration for Tan Lerida
// Generated from Firebase Console — do not commit to public repositories

import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyCuIVLppaHJa_RDiQ628TsqrM-DCVgk07s",
  authDomain: "tan-lerida.firebaseapp.com",
  projectId: "tan-lerida",
  storageBucket: "tan-lerida.firebasestorage.app",
  messagingSenderId: "367820639415",
  appId: "1:367820639415:web:5f8ebd6e77cb5823cc9132",
  measurementId: "G-4CB9NZ7SYJ"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { app, analytics };
