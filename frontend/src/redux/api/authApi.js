import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { setPosts } from "../features/userSlice";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
  }),
  endpoints: (builder) => ({
    forTestEndPoint: builder.query({
      query: () => "/user-list",
      transformResponse: (response) => response,
      onQueryStarted: async (arg, { dispatch, queryFulfilled }) => {
        try {
          const { data } = await queryFulfilled;
          dispatch(setPosts(data));
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
    }),
  }),
});

export const { useForTestEndPointQuery } = authApi;
