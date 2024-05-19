import React, {useEffect} from 'react';
import { Space, Table, Tag, Typography } from 'antd';
import axios from 'axios';




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
    title: 'Доступы',
    key: 'access',
  },
  {
    title: 'Действия',
    key: 'action',
    render: (_, record) => (
      <Space size="middle">
        <a>Изменить</a>
        <a>Удалить</a>
      </Space>
    ),
  },
];



const Data = () => {

  const fetchData = () => {
    axios.get('http://127.0.0.1/api/data/my').then(result => {
      console.log('result', result);
    })
  };

  // useEffect
  return(
    <>
      <Typography>Hello</Typography>
    </>
  )
  // <Table columns={columns} dataSource={data}/>
};

export default Data;