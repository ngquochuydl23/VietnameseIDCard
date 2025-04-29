<script>
export default {
  data: () => {
    return {
      copyrightDate: new Date().getFullYear(),
      projectName: "Trích xuất căn cước công dân",
      author: "Nguyễn Quốc Huy & Lê Thị Thu Hương",
    };
  },
};
</script>

<template>
  <div class="flex justify-center items-center text-center">
    <div class="font-[500] text-lg text-ternary-dark dark:text-ternary-light">
      &copy; {{ copyrightDate }}.
      <a
        href="https://github.com/realstoman/vuejs-tailwindcss-portfolio"
        target="__blank"
        class="font-[600] hover:underline hover:text-indigo-600 dark:hover:text-indigo-300 duration-500"
      >
        {{ projectName }}
      </a>
      . Phát triển bởi
      <a
        href="https://stoman.me"
        target="__blank"
        class="font-[500] text-secondary-dark dark:text-secondary-light uppercase hover:underline hover:text-indigo-600 dark:hover:text-indigo-300 duration-500"
        >{{ author }}</a
      >
    </div>
  </div>
</template>

<style lang="scss" scoped></style>
