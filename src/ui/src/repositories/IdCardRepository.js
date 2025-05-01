import { axiosInstance } from "./http";

export const extractIdCardInfo = (formData) =>
  axiosInstance.post(`/idcard-extract`, formData);
