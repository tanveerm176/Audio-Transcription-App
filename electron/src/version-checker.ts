import { app } from 'electron';
import https from 'https';

interface ReleaseInfo {
  tag_name: string;
  html_url: string;
  published_at: string;
}

export async function checkForUpdates(): Promise<{
  hasUpdate: boolean;
  latestVersion: string;
  currentVersion: string;
  downloadUrl?: string;
}> {
  const currentVersion = app.getVersion();
  
  return new Promise((resolve) => {
    const options = {
      hostname: 'api.github.com',
      path: '/repos/YOUR_USERNAME/transcription-app/releases/latest',
      headers: {
        'User-Agent': 'Clinical-Transcription-App'
      }
    };

    https.get(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const release: ReleaseInfo = JSON.parse(data);
          const latestVersion = release.tag_name.replace('v', '');
          const hasUpdate = compareVersions(latestVersion, currentVersion) > 0;

          resolve({
            hasUpdate,
            latestVersion,
            currentVersion,
            downloadUrl: hasUpdate ? release.html_url : undefined
          });
        } catch (error) {
          resolve({
            hasUpdate: false,
            latestVersion: currentVersion,
            currentVersion
          });
        }
      });
    }).on('error', () => {
      resolve({
        hasUpdate: false,
        latestVersion: currentVersion,
        currentVersion
      });
    });
  });
}

function compareVersions(v1: string, v2: string): number {
  const parts1 = v1.split('.').map(Number);
  const parts2 = v2.split('.').map(Number);

  for (let i = 0; i < 3; i++) {
    if (parts1[i] > parts2[i]) return 1;
    if (parts1[i] < parts2[i]) return -1;
  }
  return 0;
}