import React from 'react';
import { View, Text } from 'react-native';
import { Circle } from 'react-native-svg';
import { AnimatedCircularProgress } from 'react-native-circular-progress';

const Gauge = ({ percentage, label, value }) => (
  <View style={{ alignItems: 'center', margin: 20 }}>
    <AnimatedCircularProgress
      size={120}
      width={10}
      fill={percentage}
      tintColor="#00e0ff"
      backgroundColor="#3d5875"
    />
    <Text style={{ marginTop: 10 }}>{label}</Text>
    <Text style={{ fontSize: 18, fontWeight: 'bold' }}>{value}</Text>
  </View>
);

export default Gauge;