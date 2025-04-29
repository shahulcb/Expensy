import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./features/userSlice";

import { authApi } from "./api/authApi";

export const store = configureStore({
  reducer: {
    auth: userReducer,
    [authApi.reducerPath]: authApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat([authApi.middleware]),
});
