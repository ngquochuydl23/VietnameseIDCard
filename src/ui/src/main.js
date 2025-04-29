import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import BackToTop from "vue-backtotop";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "./assets/css/app.css";
const feather = require("feather-icons");
feather.replace();

const app = createApp(App);
app.use(ElementPlus);
app.use(router);
app.use(BackToTop);
app.mount("#app");

const appTheme = localStorage.getItem("theme");

// Check what is the active theme and change theme when user clicks on the theme button in header.
if (
  appTheme === "dark" &&
  document.querySelector("body").classList.contains("app-theme")
) {
  document.querySelector("body").classList.add("bg-primary-dark");
} else {
  document.querySelector("body").classList.add("bg-secondary-light");
}
