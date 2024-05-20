import React, { useState } from 'react';
import { LockOutlined, UserOutlined, LoginOutlined, SafetyOutlined } from '@ant-design/icons';
import { Button, Form, Input, Row, Col, Typography, message} from 'antd';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
const { Title } = Typography;
import Cookies from 'universal-cookie';

const axios_config = {
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  withCredentials: true,
};


const Login = () => {

  const navigate = useNavigate();

  const onLogin = async (values) => {
    const body = new FormData();
    var username = values["username"]
    var password = values["password"]
    body.append("username", username);
    body.append("password", password);

    await axios.post('http://127.0.0.1:8000/api/user/login', body, axios_config)
    .then(function (response) {
      navigate("/")
      return(
        message.open({
          type: 'success',
          content: 'Добро пожаловать! 😃',
          duration: 1.5,
        })
      )
    })
    .catch(function (error) {
      if (error.response.status == 400){
        return(
          message.open({
            type: 'warning',
            content: 'Неверный логин ил пароль 😕',
            duration: 2,
          })
        );
      } else {
        return(
          message.open({
            type: 'error',
            content: 'Возникла ошибка 😭',
            duration: 2,
          })
        );
      }
      
    });
  };  

  return (
    <>
      <Row className='place-content-center'>
        <Col span={8} offset={8}>
          <Title level={2}>
          <SafetyOutlined
            style={{
              marginRight: 2,
            }}
          />
            DataSec
          </Title>
          <Form
            name="normal_login"
            className="login-form"
            initialValues={{
              remember: true,
            }}
            onFinish={onLogin}
          >
            <Form.Item
              name="username"
              rules={[
                {
                  type: 'email',
                  message: 'Почта введена некорректно!',
                },
                {
                  required: true,
                  message: 'Введите электронную почту!',
                },
              ]}
            >
              <Input
                prefix={<UserOutlined className="site-form-item-icon" />}
                placeholder="Элекронная почта"
                name='username'
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[
                {
                  required: true,
                  message: 'Введите пароль!',
                },
              ]}
            >
              <Input.Password
                prefix={<LockOutlined className="site-form-item-icon" />}
                type="password"
                placeholder="Пароль"
                name='password'
              />
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                <LoginOutlined />
                Войти
              </Button>
            </Form.Item>
          </Form>
        </Col>
      </Row>
    </>
  );
};
export default Login;