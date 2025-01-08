import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { makeARequest } from './api'; // Adjust the path to your `api.ts` file

interface ApiData {
  id: string;
  name: string;
  status: string;
}

const App: React.FC = () => {
  const [data, setData] = useState<ApiData[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
        const apiData = await makeARequest();
        setData(apiData);
    };

    fetchData();
  }, []);

  if (error) {
    return <Text>Error: {error}</Text>;
  }

  return (
    <View style={styles.container}>
      {data.map((item) => (
        <View key={item.id} style={styles.item}>
          <Text>{item.name}</Text>
          <Text>Status: {item.status}</Text>
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  item: {
    marginBottom: 10,
  },
});

export default App;
