<template>
  <div class="container mx-auto" v-loading="loading">
    <div class="w-full block md:grid grid-cols-12 gap-4">
      <div class="w-full md:col-span-4 col-span-12 flex flex-col gap-3">
        <div class="section">
          <h4 class="section-title">Tải ảnh mặt trước</h4>
          <div
            class="idcard-frame-container"
            @click="imagePicker('front-idcard-picker')"
          >
            <input
              id="front-idcard-picker"
              type="file"
              @change="(e) => onPickedImage(e, 'front-idcard-picker')"
            />
            <img
              v-if="!frontIdCard"
              class="placeholder"
              src="../assets/images/camera_placeholder.png"
            />
            <img v-else class="idcard" :src="frontIdCard.url" />
            <button
              class="close-btn"
              @click="
                (e) => {
                  e.stopPropagation();
                  frontIdCard = null;
                }
              "
            >
              &#10006;
            </button>
          </div>
        </div>
        <div class="section">
          <h4 class="section-title">Tải ảnh mặt sau</h4>
          <div
            class="idcard-frame-container"
            @click="imagePicker('back-idcard-picker')"
          >
            <input
              id="back-idcard-picker"
              type="file"
              @change="(e) => onPickedImage(e, 'back-idcard-picker')"
            />
            <img
              v-if="!backIdCard"
              class="placeholder"
              src="../assets/images/camera_placeholder.png"
            />
            <img v-else class="idcard" :src="backIdCard.url" />
            <button
              class="close-btn"
              @click="
                (e) => {
                  e.stopPropagation();
                  backIdCard = null;
                }
              "
            >
              &#10006;
            </button>
          </div>
        </div>

        <div class="section">
          <h4 class="section-title">Lưu ý</h4>
          <ul class="cautions">
            <li>
              Sử dụng cùng một loại giấy tờ để chụp ảnh mặt trước và mặt sau.
            </li>
            <li>Bảo đảm giấy tờ không bị mất góc, bẫm lỗ.</li>
            <li>Bảo đảm ánh sáng không quá chói hay quá tối</li>
            <li>Là bản gốc và còn hạn.</li>
          </ul>
        </div>
        <button
          :loading="true"
          :disabled="!frontIdCard || !backIdCard"
          @click="extractIdCard"
          class="extract-info-button"
        >
          Trích xuất thông tin
        </button>
        <button
          @click="
            (e) => {
              clearInput();
              clearOutput();
            }
          "
          class="reset-button"
        >
          Xóa
        </button>
      </div>
      <div class="w-full md:col-span-8 col-span-12 md:mt-0 mt-4">
        <form class="flex flex-col gap-4">
          <div class="section">
            <h4 class="section-title">Thông tin chung</h4>
            <div class="grid grid-cols-12 w-full gap-3">
              <div class="field-container col-span-12 md:col-span-6">
                <span class="label">Họ và tên</span>
                <el-input
                  class="field"
                  clearable
                  placeholder="Nhập họ tên"
                  v-model="frontIdCardResult.full_name"
                />
              </div>
              <div class="field-container col-span-12 md:col-span-6">
                <span class="label">Ngày sinh</span>
                <el-date-picker
                  clearable
                  style="width: 100%"
                  :suffix-icon="Calendar"
                  v-model="frontIdCardResult.date_of_birth"
                  type="date"
                  format="DD/MM/YYYY"
                  :popper-options="{
                    placement: 'bottom-start',
                  }"
                  placeholder="Nhập ngày sinh"
                />
              </div>
              <div class="field-container col-span-12 md:col-span-6">
                <span class="label">Giới tính</span>
                <el-select
                  clearable
                  placeholder="Chọn giới tính"
                  v-model="frontIdCardResult.sex"
                >
                  <el-option
                    class="option"
                    v-for="item in Gender"
                    :key="item"
                    :label="item"
                    :value="item"
                  />
                </el-select>
              </div>
              <div class="field-container col-span-12 md:col-span-6">
                <span class="label">Quốc tịch</span>
                <el-select
                  clearable
                  placeholder="Chọn quốc tịch"
                  v-model="frontIdCardResult.nationality"
                >
                  <el-option
                    class="option"
                    v-for="item in Country"
                    :key="item"
                    :label="item"
                    :value="item"
                  />
                </el-select>
              </div>
              <div class="field-container col-span-12">
                <span class="label">Địa chỉ thường trú</span>
                <el-input
                  clearable
                  placeholder="Nhập địa chỉ thường trú"
                  v-model="frontIdCardResult.place_of_residence"
                />
              </div>
              <div class="field-container col-span-12">
                <span class="label">Nguyên quán</span>
                <el-input
                  clearable
                  placeholder="Nhập nguyên quán"
                  v-model="frontIdCardResult.place_of_origin"
                />
              </div>
            </div>
          </div>
          <div class="section">
            <h4 class="section-title">Căn cước công dân</h4>
            <div class="grid grid-cols-12 w-full gap-3">
              <div class="field-container col-span-12 md:col-span-6">
                <span class="label">Mã số căn cước</span>
                <el-input
                  class="field"
                  clearable
                  placeholder="Nhập số cccd"
                  v-model="frontIdCardResult.id"
                />
              </div>
              <div class="field-container col-span-12 md:col-span-6">
                <span class="label">Nơi cấp giấy tờ</span>
                <el-select
                  clearable
                  placeholder="Chọn quốc tịch"
                  v-model="backIdCardResult.issue_place"
                >
                  <el-option
                    class="option"
                    v-for="item in IssuePlaces"
                    :key="item"
                    :label="item"
                    :value="item"
                  />
                </el-select>
              </div>
              <div class="field-container col-span-12 md:col-span-6">
                <span class="label">Ngày cấp</span>
                <el-date-picker
                  v-model="backIdCardResult.issue_date"
                  style="width: 100%"
                  :suffix-icon="Calendar"
                  type="date"
                  format="DD/MM/YYYY"
                  clearable
                  placeholder="Nhập ngày cấp"
                />
              </div>
              <div class="field-container col-span-12 md:col-span-6">
                <span class="label">Ngày hết hạn</span>
                <el-date-picker
                  v-model="frontIdCardResult.date_of_expiry"
                  style="width: 100%"
                  :suffix-icon="Calendar"
                  type="date"
                  clearable
                  format="DD/MM/YYYY"
                  placeholder="Nhập ngày hết hạn"
                />
              </div>
              <div class="field-container col-span-12">
                <span class="label">Đặc điểm nhận dạng</span>
                <el-input
                  clearable
                  placeholder="Nhập đặc điểm nhận dạng"
                  v-model="backIdCardResult.personal_identification"
                />
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { Calendar } from "@element-plus/icons-vue";
import { Gender, Country, IssuePlaces } from "../data/idcardData";
import moment from "moment";
import { ElNotification } from "element-plus";
import { extractIdCardInfo } from "../repositories/IdCardRepository";

export default {
  name: "Home",
  components: {},
  data() {
    return {
      Calendar,
      Country,
      Gender,
      IssuePlaces,
      frontIdCard: null,
      backIdCard: null,

      loading: false,
      frontIdCardResult: {
        id: null,
        full_name: null,
        date_of_birth: null,
        sex: null,
        nationality: null,
        place_of_residence: null,
        date_of_expiry: null,
        place_of_origin: null,
      },
      backIdCardResult: {
        issue_place: null,
        issue_date: null,
        personal_identification: null,
      },
    };
  },

  methods: {
    imagePicker(domId) {
      document.getElementById(domId)?.click();
    },
    onPickedImage(event, domId) {
      const file = event.target.files[0];
      if (domId === "back-idcard-picker") {
        this.backIdCard = {
          file,
          url: URL.createObjectURL(file),
        };
      } else {
        this.frontIdCard = {
          file,
          url: URL.createObjectURL(file),
        };
      }
    },
    clearInput() {
      this.frontIdCard = null;
      this.backIdCard = null;
    },
    clearOutput() {
      this.frontIdCardResult = {
        id: null,
        full_name: null,
        date_of_birth: null,
        sex: null,
        nationality: null,
        place_of_residence: null,
        date_of_expiry: null,
        place_of_origin: null,
      };
      this.backIdCardResult = {
        issue_place: null,
        issue_date: null,
        personal_identification: null,
      };
    },
    async extractIdCard() {
      this.clearOutput();

      if (!this.frontIdCard || !this.backIdCard) return;
      this.loading = true;

      const formData = new FormData();
      formData.append("front_card", this.frontIdCard?.file);
      formData.append("back_card", this.backIdCard?.file);

      try {
        const result = await extractIdCardInfo(formData);
        if (result.front) {
          this.frontIdCardResult = {
            ...result.front,
            date_of_birth: moment(result.front.date_of_birth, "DD/MM/YYYY"),
          };
        }

        if (result.back) {
          this.backIdCardResult = {
            ...result.back,
            issue_date: moment(result.back.issue_date, "DD/MM/YYYY"),
          };
        }
        this.loading = false;

        ElNotification({
          title: "Thành công",
          message: "Trích xuất thông tin thành công.",
          type: "success",
        });
      } catch (error) {
        this.loading = false;
        if (error.response) {
          console.error("Backend responded with error:", error.response.data);
          ElNotification({
            title: "Lỗi",
            message: error.response.data.message || "Lỗi không xác định",
            type: "error",
          });
        } else {
          console.error("Network error or no response:", error.message);
          ElNotification({
            title: "Lỗi",
            message: "Lỗi máy chủ",
            type: "error",
          });
        }
      }
    },
  },
};
</script>
<style scoped>
.alert {
  font-weight: bold;
}

.el-alert {
  margin: 20px 0 0;
}
.el-alert:first-child {
  margin: 0;
}

.reset-button {
  width: 100%;
  margin-top: 5px;
  border-radius: 5px;
  height: 45px;
  color: gray;
  border: 1px solid gray;
}

.extract-info-button {
  width: 100%;
  margin-top: 10px;
  height: 45px;
  color: white;
  background-color: #08ac4b;
  border-radius: 5px;
}

.extract-info-button:disabled {
  background-color: #d3d3d3;
}

.option {
  font-weight: 500;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}
.el-input :deep(.el-input__inner) {
  font-size: 14px;
}
.field-container {
  display: flex;
  gap: 5px;
  width: 100%;
  flex-direction: column;
}

.field-container .field {
  width: 100%;
  font-size: 13px;
}

.field-container .label {
  font-size: 14px;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.section .idcard-frame-container {
  display: flex;
  width: 100%;
  isolation: isolate;
  position: relative;
  align-items: center;
  overflow: hidden;
  justify-content: center;
  border: 2px #d3d3d3 dashed;
  aspect-ratio: 16/9;
  background-color: whitesmoke;
  border-radius: 20px;
}

.section .idcard-frame-container input {
  display: none;
}

.section .idcard-frame-container:hover {
  background-color: #d3d3d3;
}

.section .idcard-frame-container .placeholder {
  width: 60px;
  height: 60px;
}

.section .idcard-frame-container .idcard {
  object-fit: contain;
  position: relative;
  width: 100%;
  height: 100%;
}

.section .idcard-frame-container .close-btn {
  position: absolute;
  width: 30px;
  height: 30px;
  z-index: 1;
  top: 10px;
  border-radius: 100px;
  background-color: white;
  right: 10px;
  padding: 5px;
  pointer-events: visible;
}

.section .section-title {
  font-size: 18px;
  font-weight: 600;
}

.section .cautions {
  padding-left: 20px;
  list-style-type: disc;
}
</style>
