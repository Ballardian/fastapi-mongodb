import { useState, useEffect } from "react";
import axios from "axios";
import { Flex } from "antd";
import HcpTable from "./components/HcpTable";
import HcpDetailDrawer from "./components/HcpDetailDrawer";

const HcpPage = () => {
  const [hcpData, setHcpData] = useState(null);
  const [selectedTableRow, setSelectedTableRow] = useState(null);

  useEffect(() => {
    fetchHcps();
  }, []);

  const fetchHcps = async (searchValue) => {
    try {
      // TODO abstract to api file
      const requestData = {
        search: searchValue?.toString(),
      };
      const response = await axios.get("http://localhost:8000/api/hcps/", {
        params: requestData,
      });
      const data = response.data.hcps;
      setHcpData(data);
    } catch (error) {
      // TODO show message to user
      // Send to Sentry etc
      console.log("error", error);
    }
  };

  const handleSelectedTableRowChange = async (selectedRecord) => {
    try {
      const recordId = selectedRecord?.id;
      // TODO abstract to api file
      const response = await axios.get(
        `http://localhost:8000/api/hcps/${recordId}`
      );
      const data = response?.data;
      setSelectedTableRow(data);
    } catch (error) {
      // TODO show message to user
      // Send to Sentry etc
      console.log("error", error);
    }
  };

  const handleDrawerClose = () => {
    setSelectedTableRow(null);
  };

  const handleSearchChange = (value) => {
    fetchHcps(value);
  };

  return (
    <Flex justify="center">
      <HcpTable
        data={hcpData}
        onSelectRow={handleSelectedTableRowChange}
        onSearch={handleSearchChange}
      />
      {selectedTableRow && (
        <HcpDetailDrawer
          data={selectedTableRow}
          onClose={handleDrawerClose}
          open={selectedTableRow}
        />
      )}
    </Flex>
  );
};

export default HcpPage;
