// import AxiosDigestAuth from '@mhoc/axios-digest-auth';
// const digestAuth = new AxiosDigestAuth({
//   username: MY_DIGEST_USERNAME,
//   password: MY_DIGEST_PASSWORD,
// });

import { MY_DIGEST_USERNAME, MY_DIGEST_PASSWORD } from '@env';
// console.log('MY_DIGEST_USERNAME:', MY_DIGEST_USERNAME);
// console.log('MY_DIGEST_PASSWORD:', MY_DIGEST_PASSWORD);

import fetch from 'react-native-digest-fetch';

// Create Digest Authentication client
const client = new DigestFetch(MY_DIGEST_USERNAME, MY_DIGEST_PASSWORD, { algorithm: 'MD5' });


/**
 * Define the structure of the API response.
 */
interface ApiResponse {
    id: string; // Replace with actual field names and types from your API
    name: string;
    status: string;
  }

// Function to make a request and log headers
export const makeARequest = async () => {
    try {
      const response = await client.fetch('https://s18.myenergi.net/cgi-jstatus-Z', {
        method: 'GET',
        headers: { Accept: 'application/json' },
      });
  
      // Log request and response headers
    console.log('Response Headers:');
        response.headers.forEach((value: string, key: string) => {
        console.log(`${key}: ${value}`);
        });
    console.log('Content-Type:', response.headers.get('content-type'));
  
      const data = await response.json();
      console.log('Response Data:', data);
  
      return data;
    } catch (error) {
      // Type guard: check if the error is an instance of Error
    if (error instanceof Error) {
        console.error('Error Message:', error.message);
      } else {
        console.error('Unknown Error:', error);
      }
      throw error;
    }
  };