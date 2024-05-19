import React, {useEffect} from 'react';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Login from './login/Login';
import Data from './data/Data';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Data/>,
  },
  {
    path: "/login",
    element: <Login/>,
  },
]);



const App = () => {
  return(
    <div className="App">
      <RouterProvider router={router} />
    </div>
  )
};

export default App;