import React, {useEffect, useState} from 'react';
import { Button, Space, Table, Tag, Row, Col, Form, Input, message, Modal, Switch } from 'antd';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { EditOutlined, DeleteOutlined, CloseOutlined, CheckOutlined, PlusOutlined, SaveOutlined} from '@ant-design/icons';
<SaveOutlined />

const Users = () => {

  //PAGE CONFIG
  useEffect(() => {
    getUsers();
    editForm.resetFields();
  },[]);

  const navigate = useNavigate();





  //EDIT MODAL
  const [editForm] = Form.useForm();
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  
  const showEditModal = (values) => {
    editForm.setFieldsValue({
      id: values.id,
      name: values.name,
      email: values.email,
      is_superuser: values.is_superuser,
    });
    setIsEditModalOpen(true);
  };
  const closeEditModal = () => {
    setIsEditModalOpen(false);
    editForm.resetFields();
  };



  



  //TABLE CONFIG
  const [users, setUsers] = useState([]);

  
  const columns = [
    {
      title: 'Имя',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Почта',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Уровень прав',
      dataIndex: 'is_superuser',
      key: 'is_superuser',
      render: (_, record) => {
        if (record.is_superuser){
          return (
            <>
              <Tag color="purple">Администратор</Tag>
            </>
          )
        } else {
          return (
            <>
              <Tag color="green">Пользователь</Tag>
            </>
          )
        }
      }
    },
    {
      title: 'Действия',
      key: 'action',
      width: 120,
      render: (_, record) => (
        <Space size="small">
          <Button
            type="default"
            shape="circle"
            icon={
              <EditOutlined />
            }
            onClick={()=> {showEditModal(record)}}
          />
          <Button
            danger
            type="default"
            shape="circle"
            icon={
              <DeleteOutlined />
            }
            onClick={() => {deleteUser(record)}}
          />
        </Space>
      ),
    },
  ];
  
  



  //AXIOS CONFIG
  const axios_config = {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    withCredentials: true,
  };
  




  //AXIOS CREATE USER
  const createUser = async (values) => {
    const body = new FormData();
    var name = values["name"]
    var email = values["email"]
    var password = values["password"]
    var is_superuser = values["is_superuser"]
    body.append("name", name);
    body.append("email", email);
    if (password == ""){
      body.append("password", null);
    } else {
      body.append("password", password);
    }
    
    body.append("is_superuser", false);
    body.append("is_active", true);
    body.append("is_verified", false);

    await axios.post('http://127.0.0.1:8000/api/user/register', body, axios_config)
    .then(function (response) {
      window.location.reload();
      return (
        message.open({
          type: 'success',
          content: 'Пользователь успешно создан 😃',
          duration: 1,
        })
      )
    })
    .catch(function (error) {
      if (error.response.status == 400){
        if (error.response.data.detail == "REGISTER_USER_ALREADY_EXISTS"){
          message.open({
            type: 'warning',
            content: 'Такой пользователь уже существует 😕',
            duration: 2,
          }) 
        } else {
          message.open({
            type: 'error',
            content: 'Запрос выполнен неудачно 😭',
            duration: 2,
          }) 
        }
      } else if (error.response.status == 401){
        navigate("/login")
        return(
          message.open({
            type: 'warning',
            content: 'Сеанс окончен 😕',
            duration: 2,
          }) 
        )
      } else if (error.response.status == 403){
        navigate("/login")
        return(
          message.open({
            type: 'warning',
            content: 'У Вас нет прав для создания пользоваелей 😕',
            duration: 2,
          }) 
        )
      } else {
        return(
          message.open({
            type: 'error',
            content: 'Возникла ошибка 😭',
            duration: 2,
          })
        );
      }
    })
  };





  //AXIOS GET USERS
  const getUsers = async () => {
    await axios.get('http://127.0.0.1:8000/api/user/all', axios_config)
    .then(function (response) {
      const users_items = [
        response.data.data.map(c => {
          return {
            id: c.id,
            name: c.name,
            email: c.email,
            is_superuser: c.is_superuser,
          }
        })
      ]
      setUsers(users_items);
    })
    .catch(function (error) {
      if (error.response.status == 401){
        navigate("/login")
        return(
          message.open({
            type: 'warning',
            content: 'Сеанс окончен 😕',
            duration: 2,
          }) 
        )
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
  }





  //AXIOS EDIT USER
  const editUser = async (values) => {
    const body = new FormData();
    var id = values["id"]
    var name = values["name"]
    var email = values["email"]
    var password = values["password"]
    var is_superuser = values["is_superuser"]
    body.append("id", parseInt(id));
    body.append("name", name);
    body.append("email", email);
    body.append("password", password);
    body.append("is_superuser", is_superuser);

    await axios.post('http://127.0.0.1:8000/api/user/edit', body, axios_config)
    .then(function (response) {
      window.location.reload();
      setIsEditModalOpen(false);
      return (
        message.open({
          type: 'success',
          content: 'Пользователь успешно изменён 😃',
          duration: 1,
        })
      )
    })
    .catch(function (error) {
      if (error.response.status == 401){
        setIsEditModalOpen(false);
        navigate("/login");
        return(
          message.open({
            type: 'warning',
            content: 'Сеанс окончен 😕',
            duration: 2,
          }) 
        )
      } else if (error.response.status == 403){
        return(
          message.open({
            type: 'warning',
            content: 'У Вас нет прав на редактирование пользователей 😕',
            duration: 4,
          }) 
        )
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





  //AXIOS DELETE USER
  const deleteUser = async (values) => {
    const body = new FormData();
    var id = values["id"]
    body.append("id", parseInt(id));

    await axios.post('http://127.0.0.1:8000/api/user/delete', body, axios_config)
    .then(function (response) {
      window.location.reload();
      return (
        message.open({
          type: 'success',
          content: 'Пользователь успешно удалён 😃',
          duration:2,
        })
      )
    })
    .catch(function (error) {
      if (error.response.status == 401){
        navigate("/login")
        message.open({
          type: 'warning',
          content: 'Сеанс окончен 😕',
          duration: 2,
        }) 
      } else if (error.response.status == 403){
        message.open({
          type: 'warning',
          content: 'У Вас нет прав на удаление пользователей 😕',
          duration: 4,
        }) 
      } else {
          message.open({
            type: 'error',
            content: 'Возникла ошибка 😭',
            duration: 2,
          })
      }
    });
  };
  
  



  return(
    <>
      <Row
        style={{
          display: 'flex',
          width: '100%',
        }}  
      >
        <Form
          name="normal_login"
          className="login-form"
          
          initialValues={{
            remember: true,
          }}
          onFinish={createUser}
          style={{
            display: 'flex',
            width: '100%',
          }}
        >
          <Space.Compact
            direction="horizontal"
            style={{
                width: '100%',
            }}
          >
            <Form.Item
              name="name"
              style={{
                width: '100%',
              }}
              rules={[
                {
                  required: true,
                  message: 'Введите имя',
                },
              ]}
            >
              <Input
                placeholder="Имя пользователя"
                name='name'
                style={{
                  width: '100%',
                }}
              />
            </Form.Item>


            <Form.Item
              name="email"
              style={{
                width: '100%',
              }}
              rules={[
                {
                  required: true,
                  message: 'Введите почту',
                },
                {
                  type: 'email',
                  message: 'Почта введена некорректно',
                },
              ]}
            >
              <Input
                placeholder="Почта пользователя"
                name='email'
                style={{
                  width: '100%',
                }}
              />
            </Form.Item>


            <Form.Item
              name="password"
              style={{
                width: '100%',
              }}
              rules={[
                {
                  required: true,
                  message: 'Введите пароль',
                },
              ]}
            >
              <Input
                placeholder="Пароль"
                name='password'
                style={{
                  width: '100%',
                }}
              />
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                <PlusOutlined />
                Добавить
              </Button>
            </Form.Item>
          </Space.Compact>
        </Form>
      </Row>






      <Row>
        <Col span={24}>
          <Table
            columns={columns}
            dataSource={users[0]}
            pagination={{
              pageSize: 10,
            }}
            scroll={{
              y: '55vh',
            }}
          />
        </Col>
      </Row>




      <Modal
        title="Изменить"
        open={isEditModalOpen}
        // onOk={handleOk}
        onCancel={closeEditModal}
        footer={[]}
      >
        <Form
          form={editForm}
          name="normal_login"
          className="login-form"
          initialValues={{
            remember: true,
          }}
          onFinish={editUser}
        >

          <Form.Item name="id" />

          <Form.Item
            name="name"
            rules={[
              {
                required: true,
                message: 'Введите имя',
              },
            ]}
          >
            <Input
              placeholder="Имя пользователя"
              name='name'
            />
          </Form.Item>


          <Form.Item
            name="email"
            rules={[
              {
                required: true,
                message: 'Введите почту',
              },
              {
                type: 'email',
                message: 'Почта введена некорректно',
              },
            ]}
          >
            <Input
              placeholder="Почта пользователя"
              name='email'
            />
          </Form.Item>


          <Form.Item
            name="password"
          >
            <Input
              placeholder="Пароль"
              name='password'
            />
          </Form.Item>


          <Form.Item
            name="is_superuser"
          >
            <Switch
              checkedChildren="Администратор"
              unCheckedChildren="Пользователь"
              name='is_superuser'
              style={{
                marginRight: 5,
              }}
            />
          </Form.Item>


          <Form.Item>
            <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                <CheckOutlined />
                  Сохранить
              </Button>,
              <Button
                type="default"
                danger
                className="login-form-button"
                onClick={closeEditModal}
              >
                <CloseOutlined />
                  Отмена
              </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
  
};

export default Users;