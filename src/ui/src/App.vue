<script>
import feather from "feather-icons";
import AppHeader from "./components/shared/AppHeader";
import AppFooter from "./components/shared/AppFooter";

export default {
  components: {
    AppHeader,
    AppFooter,
  },
  data: () => {
    return {
      appTheme: localStorage.getItem("theme"),
    };
  },
  mounted() {
    feather.replace();
  },
  updated() {
    feather.replace();
  },
};
</script>

<template>
  <div :class="appTheme" class="pt-0.5">
    <AppHeader />
    <transition name="fade" mode="out-in">
      <router-view :theme="appTheme" />
    </transition>
    <back-to-top
      visibleoffset="500"
      right="30px"
      bottom="20px"
      class="shadow-lg"
    >
      <i data-feather="chevron-up"></i>
    </back-to-top>
    <AppFooter />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.vue-back-to-top {
  @apply p-2  text-white transition
        duration-500
        ease-in-out
        transform
        hover:-translate-y-1 hover:scale-110;
  background-color: #08ac4b;
  border-radius: 10px;
  font-size: 22px;
  height: 40px;
  width: 40px;
  line-height: 22px;
}

.fade-enter-active {
  animation: coming 0.4s;
  animation-delay: 0.2s;
  opacity: 0;
}

.fade-leave-active {
  animation: going 0.4s;
}

@keyframes going {
  from {
    transform: translateX(0);
  }

  to {
    transform: translateX(-10px);
    opacity: 0;
  }
}

@keyframes coming {
  from {
    transform: translateX(-10px);
    opacity: 0;
  }

  to {
    transform: translateX(0px);
    opacity: 1;
  }
}
</style>
