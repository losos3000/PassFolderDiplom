import React from 'react';
import {createBrowserRouter,RouterProvider,} from "react-router-dom";
import Login from './login/Login';
import Data from './data/Data';
import Users from './users/Users';
import LayoutBlock from './layout/LayoutBlock';

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <LayoutBlock>
        <Data/>
      </LayoutBlock>
    ),
  },
  {
    path: "/login",
    element: <Login/>,
  },
  {
    path: "/users",
    element: (
      <LayoutBlock>
        <Users/>
      </LayoutBlock>
    ),
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