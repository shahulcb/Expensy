import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  posts: [],
};

export const userSlice = createSlice({
  initialState,
  name: "userSlice",
  reducers: {
    setPosts(state, action) {
      state.posts = action.payload;
    },
  },
});

export default userSlice.reducer;

export const { setPosts } = userSlice.actions;
