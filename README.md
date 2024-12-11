# 🌟 **Hexa-Tile Adventure** 🌟  

<div align="center">
  <img src="hex_01.png" alt="Hexa-Tile Game" width="400">
  <img src="pencil_sort_01.png" alt="Pencil Sort" width="200">
  <p><i>육각형 퍼즐과 창의성의 만남! (왼: pygame-hex_tile_game), (오: pencil sort)</i></p>
</div>

---

## 🎮 **게임 개발 계기**

### **왜 Hexa-Tile Adventure를 만들었나요?**

**Hexa-Tile Adventure**는 퍼즐 게임의 매력을 최대한 활용하며, **광고 없는 몰입 경험**을 제공하기 위해 제작되었습니다.  
평소 [Pencil Sort](https://apps.apple.com)라는 게임을 즐기며 광고와 제한적인 플레이에 불편함을 느껴 직접 제작하기로 결심했습니다.

### **💡 개발 목표**
1. **완벽한 플레이 자유도 제공**: 광고 없이 순수 게임에 집중.
2. **퍼즐 메커니즘의 창의적 확장**: 육각형 타일과 연결 시스템을 더 복잡하고 도전적으로 설계.
3. **Python 및 Pygame 학습**: 단순한 게임 제작을 넘어 코딩 실력을 한 단계 향상.

---

## 🎮 **게임 소개**

**Hexa-Tile Adventure**는 전략적 사고와 창의력을 요구하는 3D 퍼즐 게임입니다.  
게임은 육각형 타일을 보드에 배치하고, **같은 색상** 타일을 연결하여 문제를 해결하는 것이 핵심입니다.

### **게임의 목표**  
- **타일 배치:** 플레이어는 보드 위에 타일을 자유롭게 배치합니다.  
- **타일 연결:** 같은 색 타일을 연결하여 점수를 획득합니다.  
- **레벨 클리어:** 도전 과제를 해결하고 다음 레벨로 넘어갑니다.  

### **특징**
1. **독창적인 육각형 타일 시스템**  
   기존의 직사각형 퍼즐이 아닌, 육각형 타일을 사용하여 새로운 도전과 재미를 제공합니다.
2. **연속적인 점수 획득 시스템**  
   연결된 타일 수가 많을수록 보너스 점수가 더해집니다.
3. **시각적 효과**  
   연결된 타일이 사라질 때 화려한 애니메이션이 플레이됩니다.

---

## 🌈 **게임의 주요 특징**

<div align="center">
  <table style="border-collapse: collapse; width: 90%; text-align: center; font-size: 16px;">
    <thead>
      <tr style="border-bottom: 2px solid #4caf50;">
        <th style="padding: 10px;">🎮 기능</th>
        <th style="padding: 10px;">✨ 상세 설명</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 10px;">육각형 타일 정렬 메커니즘</td>
        <td style="padding: 10px;">플레이어는 육각형 타일을 전략적으로 배치하여 연결합니다.</td>
      </tr>
      <tr style="background-color: #f9f9f9;">
        <td style="padding: 10px;">타일 연결 및 점수 시스템</td>
        <td style="padding: 10px;">6개 이상의 같은 색 타일을 연결하면 사라지고 점수를 획득합니다.</td>
      </tr>
      <tr>
        <td style="padding: 10px;">단계별 레벨 업</td>
        <td style="padding: 10px;">점점 더 복잡하고 도전적인 타일 세트를 만납니다.</td>
      </tr>
      <tr style="background-color: #f9f9f9;">
        <td style="padding: 10px;">다양한 색상 타일</td>
        <td style="padding: 10px;">6가지 색상을 포함하며, 조합에 따라 다양한 시각적 효과가 발생합니다.</td>
      </tr>
      <tr>
        <td style="padding: 10px;">보너스 타일 보드</td>
        <td style="padding: 10px;">레벨이 올라갈수록 사용할 수 있는 타일보드가 늘어납니다.</td>
      </tr>
    </tbody>
  </table>
</div>

---

## 🛠️ **게임 가이드**

### **1️⃣ 시작하기**
#### **목표**  
- 육각형 타일을 보드에 배치하고, **같은 색 타일**을 연결하여 점수를 획득하세요.
- 6개 이상의 같은 색 타일이 연결되면 사라지며 **점수가 추가**됩니다.

#### **레벨 업 규칙**
- 모든 타일을 정리한 후, 더 높은 난이도에서 새로운 도전에 도전하세요.
- 각 레벨마다 색상 패턴과 배치가 복잡해집니다.

---

### **2️⃣ 조작법**
#### 🚀 기본 조작
- **드래그 앤 드롭:** 마우스로 타일을 클릭하여 원하는 위치로 이동합니다.

#### 🌀 고급 기능
- **자동 정렬:** 타일을 보드에 맞추어 자동으로 배치됩니다.
- **타일 제거:** 불필요한 타일을 선택하여 제거하고 새로운 타일을 요청할 수 있습니다.

---

## 📦 **설치 및 실행 방법**

1. **레포지토리 클론**
   ```bash
   git clone https://github.com/your-username/Hexa-Tile-Adventure.git
   cd Hexa-Tile-Adventure

개발 중 느낀 점
Pygame의 타일 연결 시스템을 구현하는 과정은 도전적이었지만, 이를 통해 Python 자료 구조를 활용하는 능력을 크게 향상할 수 있었습니다.
특히 육각형 타일의 배치를 위한 알고리즘 설계는 기존 퍼즐 게임과 차별화된 흥미로운 작업이었습니다.
향후 추가 기능
멀티플레이어 모드
다른 플레이어와 점수를 경쟁할 수 있는 실시간 모드를 추가할 예정입니다.
커스터마이징
사용자가 타일 색상, 배경 테마를 자유롭게 변경할 수 있는 옵션을 제공할 계획입니다.
