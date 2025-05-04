
import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList, StyleSheet } from 'react-native';
import * as Notifications from 'expo-notifications';
import Constants from 'expo-constants';

export default function App() {
  const [signals, setSignals] = useState([]);

  const fetchSignals = async () => {
    try {
      const response = await fetch('https://your-api-url.com/signals');
      const data = await response.json();
      setSignals(data);
    } catch (error) {
      console.error("Error fetching signals:", error);
    }
  };

  const handleAction = async (signalId, action) => {
    try {
      await fetch(`https://your-api-url.com/signals/${signalId}/${action}`, {
        method: 'POST'
      });
      fetchSignals();
    } catch (error) {
      console.error("Error sending action:", error);
    }
  };

  const registerForPushNotificationsAsync = async () => {
    if (Constants.isDevice) {
      const { status: existingStatus } = await Notifications.getPermissionsAsync();
      let finalStatus = existingStatus;
      if (existingStatus !== 'granted') {
        const { status } = await Notifications.requestPermissionsAsync();
        finalStatus = status;
      }
      if (finalStatus !== 'granted') {
        alert('Failed to get push token for push notification!');
        return;
      }
      const token = (await Notifications.getExpoPushTokenAsync()).data;
      console.log("Expo Push Token:", token);
      // You can POST this token to your FastAPI backend here
    } else {
      alert('Must use physical device for Push Notifications');
    }
  };

  useEffect(() => {
    fetchSignals();
    registerForPushNotificationsAsync();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <Text style={styles.title}>Signal: {item.epic}</Text>
      <Text>Decision: {item.gpt_decision}</Text>
      <View style={styles.buttonRow}>
        <Button title="✅ Confirm" onPress={() => handleAction(item.id, 'confirm')} />
        <Button title="❌ Reject" onPress={() => handleAction(item.id, 'reject')} />
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.header}>📲 Trading Assistant</Text>
      <FlatList
        data={signals}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderItem}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: 50, paddingHorizontal: 16 },
  header: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  card: { padding: 15, marginVertical: 8, backgroundColor: '#f0f0f0', borderRadius: 10 },
  title: { fontSize: 18, fontWeight: 'bold' },
  buttonRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 10 }
});
