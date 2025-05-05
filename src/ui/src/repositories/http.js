import axios from "axios";
import _ from "lodash";

export const axiosInstance = axios.create({ baseURL: '/api/', responseType: "json" });

axiosInstance.interceptors.request.use(
  function (config) {
    config.headers["Access-Control-Allow-Origin"] = "*";
    config.headers["Content-Type"] = "application/json";
    if (config.data instanceof FormData) {
      config.headers["Content-Type"] = `multipart/form-data`;
    }

    config.headers["accept"] = `application/json`;
    config.headers["X-Requested-With"] = `XMLHttpRequest`;
    return config;
  },
  function (error) {
    console.log(error);
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => response.data.result,
  (error) => {
    if (_.has(error, "response.data.error")) {
      console.log(error);
      const responseErr = _.get(error, "response.data.error");
      console.log("http.interceptors.response", { responseErr });
      return Promise.reject(responseErr);
    }
    return Promise.reject(error);
  }
);
