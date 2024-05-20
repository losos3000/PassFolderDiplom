import React, { Children, useState, useEffect } from 'react';
import { Typography, Layout, Menu, theme, Button } from 'antd';
const { Header, Content, Footer } = Layout;
const { Title, Text } = Typography;
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import { FolderOutlined, TeamOutlined, UserOutlined, SafetyOutlined, LogoutOutlined, MailOutlined } from '@ant-design/icons';

const LayoutBlock = ({children}) => {

  //PAGE CONFIG
  useEffect(() => {
    getMe()
  },[]);

  const navigate = useNavigate();


  //ME CONFIG
  const [me, setMe] = useState([]);





  //AXIOS CONFIG
  const axios_config = {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'//'application/x-www-form-urlencoded'
    },
    withCredentials: true,
  };
  
  
  //AXIOS GET ME
  const getMe = async () => {
    await axios.get('http://127.0.0.1:8000/api/user/me', axios_config)
    .then(function (response) {
      const me_items = [
        response.data.data.map(c => {
          return {
            id: c.id,
            name: c.name,
            email: c.email,
            is_superuser: c.is_superuer,
          }
        })
      ]
      setMe(me_items[0][0])
    })
  }


  //AXIOS LOGOUT
  const logout = () => {
    axios.post('http://127.0.0.1:8000/api/user/logout', axios_config)
    .then(function (response) {
      console.log(response)
      navigate("/login");
    })
    .catch(function (error) {
      if (error.response.status == 401){
        return navigate("/login");
      } else {
        return navigate("/login");
      }
    }) 
  }




  //COLOR CONFIG
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();



  return (
    <>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          backgroundColor: 'black',
          paddingLeft: 30,
          paddingRight: 30,
          maxWidth: '100%',
        }}
      >
        <div
          style={{
            display: 'flex',
          }}
        >
          <Title  level={2} style={{color: 'white', marginRight: '50px', marginTop: '10px'}}>
          <SafetyOutlined
            style={{
              marginRight: 2,
            }}
          />
            DataSec
          </Title>
        </div>
        

        <div
          style={{
            flex: 1,
          }}
        >
          <Button type="link" size="large" style={{color: 'white'}} onClick={()=>{navigate("/")}}>
            <FolderOutlined />
            Данные
          </Button>
          <Button type="link" size="large" style={{color: 'white'}} onClick={()=>{navigate("/users")}}>
            <TeamOutlined />
            Пользователи
          </Button>
        </div>


        <div
          style={{
            display: 'flex',
          }}
        >
            <Button
            type="link"
            size="large"
            style={{
              color: 'white'
              }}
          >
            <UserOutlined/>
            {me.name}
          </Button>

          <Button
            type="link"
            size="large"
            style={{
              color: 'white'
              }}
          >
            <MailOutlined />
            {me.email}
          </Button>

          <Button
            type="link"
            size="large"
            style={{
              color: 'white'
              }}
            onClick={logout}
          >
            <LogoutOutlined />
            Выйти
          </Button>
        </div>

      </div>

      <div>
        <div
          style={{
            background: colorBgContainer,
            minHeight: '70vh',
            padding: 24,
            borderRadius: borderRadiusLG,
          }}
        >
          {children}
        </div>
      </div>


      {/* <div
        style={{
          textAlign: 'center',
        }}
      >
        Дипломная работа | Голиков А.Д. Группа АБс-922 | Кафедра защиты информации НГТУ 2024
      </div> */}

    </>
  );
};
export default LayoutBlock;