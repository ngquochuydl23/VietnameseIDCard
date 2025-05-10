<script>
import feather from "feather-icons";
// import FooterCopyright from "./FooterCopyright.vue";
import { socialLinks } from "../../data/socialLinks";

export default {
  //   components: { FooterCopyright },
  data() {
    return {
      socials: socialLinks,
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
  <div class="container mx-auto">
    <div
      class="pt-20 sm:pt-30 pb-8 mt-20 border-t-2 border-primary-light dark:border-secondary-dark"
    >
      <!-- Footer social links -->
      <div class="flex flex-col justify-center items-center mb-12 sm:mb-20">
        <p
          class="text-2xl sm:text-4xl font-semibold text-[#000] dark:text-primary-light mb-5"
        >
          Báo cáo cuối kỳ • Nhóm 1
        </p>
        <p
          class="text-xl font-semibold text-[#000] dark:text-primary-light mb-5"
        >
          Đề tài: ỨNG DỤNG MÔ HÌNH HỌC SÂU TRÍCH XUẤT THÔNG TIN CĂN CƯỚC CÔNG
          DÂN
        </p>

        <div style="width: 400px">
          Giảng viên hướng dẫn: Ths. Võ Quang Hoàng Khang
        </div>
        <div style="width: 400px">
          Thành viên nhóm:
          <ul>
            <li>21112801 - Nguyễn Quốc Huy</li>
            <li>21111531 - Lê Thị Thu Hương</li>
          </ul>
        </div>
        <!-- <ul class="flex gap-4 sm:gap-8">
          <a
            v-for="social in socials"
            :key="social.id"
            :href="social.url"
            target="__blank"
            class="text-gray-400 hover:text-indigo-500 dark:hover:text-indigo-400 cursor-pointer rounded-lg bg-gray-50 dark:bg-ternary-dark hover:bg-gray-100 shadow-sm p-4 duration-500"
          >
            <i :data-feather="social.icon" class="w-5 sm:w-8 h-5 sm:h-8"></i>
          </a>
        </ul> -->
      </div>

      <!-- Footer copyright -->
      <!-- <FooterCopyright /> -->
    </div>
  </div>
</template>

<style scoped></style>
