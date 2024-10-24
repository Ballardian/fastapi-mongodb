import React from "react";
import { Table, Row, Input, Space } from "antd";
const { Search } = Input;

const columns = [
  {
    title: "ID",
    dataIndex: "id",
    key: "id",
  },
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "Status",
    dataIndex: "status",
    key: "status",
  },
  {
    title: "Address",
    dataIndex: "address_link",
    key: "address",
    render: (record) => {
      return Object.entries(record).map(([key, value]) => (
        <Row>{`${key}: ${value}`}</Row>
      ));
    },
  },
  {
    title: "Country Code",
    dataIndex: "countryIsoCode",
    key: "countryCode",
  },
];

const HcpTable = ({ data, loading, onSelectRow, searchValue, onSearch }) => (
  <Space direction="vertical" style={{ width: "80%" }}>
    <Search
      allowClear
      defaultValue={searchValue}
      placeholder="Search by HCP name"
      onSearch={(value) => onSearch(value)}
      style={{
        width: 300,
        marginTop: 20,
      }}
    />
    <Table
      // TODO add loading
      loading={loading}
      columns={columns}
      dataSource={data}
      title={() => "Health Care Providers"}
      onRow={(record) => {
        return {
          onClick: () => {
            onSelectRow(record);
          },
        };
      }}
      rowKey="id"
      bordered
    />
  </Space>
);

export default HcpTable;
