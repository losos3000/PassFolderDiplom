import React, {useEffect, useState} from 'react';
import { Button, Space, Table, Tag, Row, Col, Form, Input, message, Modal  } from 'antd';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { EditOutlined, DeleteOutlined, CloseOutlined, CheckOutlined, PlusOutlined, SaveOutlined} from '@ant-design/icons';
<SaveOutlined />

const Data = () => {

  //PAGE CONFIG
  useEffect(() => {
    getData()
  },[]);

  const navigate = useNavigate();





  //EDIT MODAL
  const [editForm] = Form.useForm();
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  
  const showEditModal = (values) => {
    editForm.setFieldsValue({
      id: values.id,
      name: values.name,
      url: values.url,
      login: values.login,
      password: values.password,
      description: values.description,
      access: values.access,
    });
    console.log(access);
    setIsEditModalOpen(true);
  };
  const closeEditModal = () => {
    setIsEditModalOpen(false);
  };



  



  //TABLE CONFIG
  const [data, setData] = useState([]);

  
  const columns = [
    {
      title: 'Название',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'URL',
      dataIndex: 'url',
      key: 'url',
    },
    {
      title: 'Логин',
      dataIndex: 'login',
      key: 'login',
    },
    {
      title: 'Пароль',
      dataIndex: 'password',
      key: 'password',
    },
    {
      title: 'Описание',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Доступы',
      key: 'access',
    },
    {
      title: 'Действия',
      key: 'action',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="default"
            shape="circle"
            icon={
              <EditOutlined />
            }
            onClick={()=> {showEditModal(record)}}//showEditModal(record)}
          />
          <Button
            danger
            type="default"
            shape="circle"
            icon={
              <DeleteOutlined />
            }
            onClick={() => {deleteData(record)}}
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
  




  //AXIOS CREATE DATA
  const createData = async (values) => {
    const body = new FormData();
    var name = values["name"]
    var url = values["url"]
    var login = values["login"]
    var password = values["password"]
    var description = values["description"]
    body.append("name", name);
    body.append("url", url);
    body.append("login", login);
    body.append("password", password);
    body.append("description", description);

    await axios.post('http://127.0.0.1:8000/api/data/add', body, axios_config)
    .then(function (response) {
      window.location.reload();
      message.open({
        type: 'success',
        content: 'Запись успешно создана 😃',
        duration: 1,
      })
    })
    .catch(function (error) {
      if (error.response.status == 401){
        navigate("/login")
        message.open({
          type: 'warning',
          content: 'Сеанс окончен 😕',
          duration: 2,
        }) 
      } else {
        message.open({
          type: 'error',
          content: 'Возникла ошибка 😭',
          duration: 2,
        })
      }
    })
  };





  //AXIOS GET DATA
  const getData = async () => {
    await axios.get('http://127.0.0.1:8000/api/data/my', axios_config)
    .then(function (response) {
      const data_items = [
        response.data.data.map(c => {
          return {
            id: c.id,
            name: c.name,
            url: c.url,
            login: c.login,
            password: c.password,
            description: c.description,
            access: c.access,
          }
        })
      ]
      setData(data_items);
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





  //AXIOS EDIT DATA
  const editData = async (values) => {
    const body = new FormData();
    var id = values["id"]
    var name = values["name"]
    var url = values["url"]
    var login = values["login"]
    var password = values["password"]
    var description = values["description"]
    var access = values["access"]
    body.append("id", id);
    body.append("name", name);
    body.append("url", url);
    body.append("login", login);
    body.append("password", password);
    body.append("description", description);
    body.append("access", access);

    console.log(access)
    console.log(body.getAll)

    // await axios.post('http://127.0.0.1:8000/api/data/edit', body, axios_config)
    // .then(function (response) {
    //   window.location.reload();
    //   setIsEditModalOpen(false);
    //   return (
    //     message.open({
    //       type: 'success',
    //       content: 'Запись успешно изменена 😃',
    //       duration: 1,
    //     })
    //   )
    // })
    // .catch(function (error) {
    //   if (error.response.status == 401){
    //     setIsEditModalOpen(false);
    //     navigate("/login");
    //     return(
    //       message.open({
    //         type: 'warning',
    //         content: 'Сеанс окончен 😕',
    //         duration: 2,
    //       }) 
    //     )
    //   } else if (error.response.status == 403){
    //     return(
    //       message.open({
    //         type: 'warning',
    //         content: 'У Вас нет прав на редактирование записи 😕',
    //         duration: 4,
    //       }) 
    //     )
    //   } else {
    //     return(
    //       message.open({
    //         type: 'error',
    //         content: 'Возникла ошибка 😭',
    //         duration: 2,
    //       })
    //     );
    //   }
    // });
  };





  //AXIOS DELETE DATA
  const deleteData = async (values) => {
    const body = new FormData();
    var id = values["id"]
    body.append("id", parseInt(id));

    await axios.post('http://127.0.0.1:8000/api/data/delete', body, axios_config)
    .then(function (response) {
      window.location.reload();
      return (
        message.open({
          type: 'success',
          content: 'Запись успешно удалена 😃',
          duration: 1,
        })
      )
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
      } else if (error.response.status == 403){
        return(
          message.open({
            type: 'warning',
            content: 'У Вас нет прав на удаление записи 😕',
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
  
  



  return(
    <>
      {/* <Row>
        <Col>
          <Button onClick={()=>{
            axios.get('http://127.0.0.1:8000/api/user/me', axios_config)
            .then(function (response) {
              console.log(response)
            })
            .catch(function (error) {
                return(
                  alert("Неизвестная ошибка. Попробуйте позже.")
                );
              })
              
            }}  
          >
            Get Me
          </Button>
        </Col>

        <Col>
          <Button
            onClick={logout}
          >
            Выйти
          </Button>
        </Col>

        <Col>
          <Button
            onClick={getcoc}
          >
            Куки
          </Button>
        </Col>
      </Row> */}





      <Row
        style={{
          display: 'flex',
        }}  
      >
        <Form
          name="normal_login"
          className="login-form"
          initialValues={{
            remember: true,
          }}
          onFinish={createData}
          style={{
            display: 'flex',
          }}
        >

          <Form.Item
            name="name"
            rules={[
              {
                required: true,
                message: 'Введите название',
              },
            ]}
          >
            <Input
              placeholder="Название"
              name='name'
            />
          </Form.Item>


          <Form.Item
            name="url"
          >
            <Input
              placeholder="URL"
              name='url'
            />
          </Form.Item>


          <Form.Item
            name="login"
          >
            <Input
              placeholder="Логин"
              name='login'
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
            name="description"
          >
            <Input
              placeholder="Описание"
              name='description'
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
        </Form>
      </Row>






      <Row>
        <Col span={24}>
          <Table
            columns={columns}
            dataSource={data[0]}
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
          onFinish={editData}
        >

          <Form.Item id="id" />
          <Form.Item access="access" />

          <Form.Item
            name="name"
            rules={[
              {
                required: true,
                message: 'Введите название',
              },
            ]}
          >
            <Input
              placeholder="Название"
              name='name'
            />
          </Form.Item>


          <Form.Item
            name="url"
          >
            <Input
              placeholder="URL"
              name='url'
            />
          </Form.Item>


          <Form.Item
            name="login"
          >
            <Input
              placeholder="Логин"
              name='login'
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
            name="description"
          >
            <Input
              placeholder="Описание"
              name='description'
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

export default Data;