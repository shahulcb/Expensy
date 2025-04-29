import { useEffect, useState } from "react";
import { useForTestEndPointQuery } from "./redux/api/authApi";

function App() {
  const [count, setCount] = useState(0);
  const { data: posts, isLoading, isError } = useForTestEndPointQuery();

  return <p className="text-3xl">{isLoading ? "loading" : "error"}</p>;
}

export default App;
