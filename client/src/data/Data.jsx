import React, {useEffect, useState} from 'react';
import { Button, Space, Table, Row, Col, Form, Input, message, Modal, Checkbox, Divider, Select  } from 'antd';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { EditOutlined, DeleteOutlined, CloseOutlined, CheckOutlined, PlusOutlined, SaveOutlined, EyeOutlined} from '@ant-design/icons';
<SaveOutlined />

const Data = () => {


  const testTable = () => {

    console.log(document.getElementById("tableForm").children)

  }






















  //PAGE CONFIG
  useEffect(() => {
    getData();
    getUsers();
  },[]);

  const navigate = useNavigate();




  //USERS
  const [users, setUsers] = useState([]);
  //ACCESS
  const [access, setAccess] = useState([]);




  //EDIT MODAL
  const [editForm] = Form.useForm();
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editAccess, setEditAccess] = useState([]);
  
  const showEditModal = (values) => {

    const access_items_table = [
      users[0].map(u=>{
        let acs_rd = ar(values.access, u);
        let acs_edt = ae(values.access, u);
        return {
          value: u.id,
          label: u.email,
          // access_read: acs_rd,
          // access_edit: acs_edt,
        }
      })
    ]

    

    const access_items_form = [
      users[0].map(u=>{
        let acs_rd = ar(values.access, u);
        let acs_edt = ae(values.access, u);
        return {
          ds_user_id: u.id,
          access_read: acs_rd,
          access_edit: acs_edt,
        }
      })
    ]


    editForm.setFieldsValue({
      id: values.id,
      name: values.name,
      url: values.url,
      login: values.login,
      password: values.password,
      description: values.description,
      access: access_items_form[0],
      
    });

    setEditAccess(access_items_table[0]);

    setIsEditModalOpen(true);
  };
  const closeEditModal = () => {
    setIsEditModalOpen(false);
  };







  //ACCESS MODAL
  
  const [isAccessModalOpen, setIsAccessModalOpen] = useState(false);

  const ar = (acs, usr) => {
    if (usr.is_superuser)
      return true;

    for (let val of acs){
      if (val.ds_user_id == usr.id){
        return (val.access_read);
      };
    };

    return false;
  }

  const ae = (acs, usr) => {
    if (usr.is_superuser)
      return true;

    for (let val of acs){
      if (val.ds_user_id == usr.id){
        return (val.access_edit);
      };
    };

    return false;
  }

  const showAccessModal = (values) => {

    const access_items = [
      users[0].map(u=>{
        let acs_rd = ar(values.access, u);
        let acs_edt = ae(values.access, u);
        return {
          id: u.id,
          name: u.name,
          email: u.email,
          is_superuser: u.is_superuser,
          access_read: acs_rd,
          access_edit: acs_edt,
        }
      })
    ]

    setAccess(access_items[0]);
    setIsAccessModalOpen(true);
  };
  const closeAccessModal = () => {
    setIsAccessModalOpen(false);
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
      width: 120,
      render: (_, record) => (
        <Button
          type="primary"
          onClick={()=> {showAccessModal(record)}}
        >
          Смотреть
        </Button>
      ),
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

    if (url == undefined)
      body.append("url", "");
    else
      body.append("url", url);

    if (login == undefined)
      body.append("login", "");
    else
      body.append("login", login);

    if (password == undefined)
      body.append("password", "");
    else
      body.append("password", password);

    if (description == undefined)
      body.append("description", "");
    else
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

    var body = JSON.stringify(values);

    await axios.post('http://127.0.0.1:8000/api/data/edit', body, axios_config)
    .then(function (response) {
      window.location.reload();
      setIsEditModalOpen(false);
      return (
        message.open({
          type: 'success',
          content: 'Запись успешно изменена 😃',
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
            content: 'У Вас нет прав на редактирование записи 😕',
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




  return(
    <>
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

      


  
      <Modal
        title="Дуступы для пользователей"
        open={isAccessModalOpen}
        onCancel={closeAccessModal}
        width={600}
        footer={[]}
      >
        <Table
          columns={[
            {
              title: 'Имя',
              dataIndex: 'name',
              key: 'name',
            },
            {
              title: 'Почта',
              dataIndex: 'email',
              key: 'email',
              width: 220,
            },
            {
              title: 'Права',
              dataIndex: 'accesses',
              key: 'accesses',
              width: 90,
              render: (_, record) => {
                if (record.access_read && record.access_edit){
                  return(
                    <>
                      <EyeOutlined style={{marginRight: 5,}}/>
                      <EditOutlined />
                    </>
                  )
                } else if (record.access_edit){
                  return(
                    <EditOutlined />
                  )
                } else if (record.access_read){
                  return(
                    <EyeOutlined />
                  )
                }
              },
            },
          ]}
          dataSource={access}
          pagination={{
            pageSize: 10,
          }}
          scroll={{
            y: '50vh',
          }}
        />
      </Modal>




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
        title="Изменить запись"
        open={isEditModalOpen}
        onCancel={closeEditModal}
        width={"70%"}
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

          <div style={{
            display: 'flex',
            alignContent: 'start',
            gap: 10,
          }}>


            <div style={{ width: '40%'}}>
              <Form.Item
                name="id"
                hidden
              />

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
                <Input.TextArea
                  autoSize={{
                    minRows: 2,
                    maxRows: 3,
                  }}
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
            </div>





            <div style={{width: '60%'}}>
            <Form.List name="access">
              {(fields, { add, remove }) => (
                <>
                  {fields.map((field) => (
                    <div>
                      <Space key={field.key}  align="baseline" size="large" direction="horizontal" style={{paddingLeft: 30}}>

                        <Form.Item name={[field.name, "ds_user_id"]} initialValue={0}>
                          <Select
                            style={{ width: 300 }}
                            options={editAccess}
                          />
                        </Form.Item>

                        <Space style={{ display: 'flex'}} align="baseline" size="small">
                          <EyeOutlined/>
                          <Form.Item name={[field.name, "access_read"]} valuePropName="checked" initialValue={true}>
                            <Checkbox/>
                          </Form.Item>
                        </Space>
                        
                        <Space style={{ display: 'flex'}} align="baseline" size="small">
                          <EditOutlined/>
                          <Form.Item name={[field.name, 'access_edit']} valuePropName="checked" initialValue={false}>
                            <Checkbox />
                          </Form.Item>
                        </Space>

                        <CloseOutlined onClick={() => remove(field.name)} style={{marginLeft: 20}}/>

                      </Space>
                      <Divider style={{marginTop: -15, marginBottom: 10}}/>
                    </div>
                  ))}
                
                  <Button type="dashed" onClick={() => add()} block>
                    Добавить права пользователю
                  </Button>
                </>
              )}
              </Form.List>
            </div>

          </div>

        </Form>
      </Modal>
    </>
  );
  
};

export default Data;