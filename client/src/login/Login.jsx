import React from 'react';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Button, Checkbox, Form, Input } from 'antd';
import axios from 'axios';


const App = () => {

  const onLogin = (_username, _password) => {
    axios.post('http://127.0.0.1:8000/api/user/login', {
      grant_type: null,
      username: _username,
      password: _password,
      scope : null,
      client_id: null,
      client_secret: null,
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  };
  

  return (
    <Form
      name="normal_login"
      className="login-form"
      initialValues={{
        remember: true,
      }}
      onFinish={onLogin}
    >
      <Form.Item
        name="email"
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
        <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Элекронная почта" />
      </Form.Item>

      <Form.Item
        name="password"
        rules={[
          {
            required: true,
            message: 'Введите пароль!',
          },
        ]}
        hasFeedback
      >
        <Input
          prefix={<LockOutlined className="site-form-item-icon" />}
          type="password"
          placeholder="Пароль"
        />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" className="login-form-button">
          Войти
        </Button>
      </Form.Item>
    </Form>
  );
};
export default App;