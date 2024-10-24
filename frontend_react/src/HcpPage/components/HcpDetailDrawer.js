import React from "react";
import { Drawer, Descriptions } from "antd";

const HcpDetailDrawer = ({ data, onClose, open }) => {
  const getStucturedItems = (data, affiliation = true) => {
    const address = Object.entries(data?.address_link)
      .map(([key, value]) => `${key}: ${value}`)
      .join(", ");

    const itemList = [
      {
        key: "1",
        label: "Name",
        children: data?.name,
      },
      {
        key: "2",
        label: "Status",
        children: data?.status,
      },
      {
        key: "3",
        label: "Address",
        children: address,
      },
    ];
    if (!affiliation) {
      itemList.push({
        key: "4",
        label: "Country Code",
        children: data?.countryIsoCode,
      });
    }
    return itemList;
  };

  return (
    <Drawer title="HCP Info" onClose={onClose} open={open} width={800}>
      <Descriptions
        title={`HCP Detail - ${data?.name}`}
        items={getStucturedItems(data, false)}
      />

      {data?.affiliations &&
        data?.affiliations.map((affiliation) => (
          <Descriptions
            title={`${affiliation?.type} - ${affiliation["child_link"]?.name}`}
            items={getStucturedItems(affiliation["child_link"])}
            style={{ marginTop: 40 }}
          />
        ))}
    </Drawer>
  );
};

export default HcpDetailDrawer;
