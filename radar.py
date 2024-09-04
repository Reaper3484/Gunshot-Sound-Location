from config import *


class Radar:
    def __init__(self, screen, simWidth, radarWidth, height) -> None:
        self.surf = pygame.Surface((radarWidth, height), SRCALPHA)
        self.radarCenter = (radarWidth // 2, height // 2)
        self.rect = self.surf.get_rect(center=self.radarCenter)
        self.screen = screen
        self.width = radarWidth
        self.simWidth = simWidth
        self.height = height
        self.lineLen = lineLen
        self.lineAngle = 0
        self.detectedPoints = []

    def draw(self):
        self.surf.fill((0, 0, 0, lineTrailAlpha), special_flags=BLEND_RGBA_MULT)
        for radar in [circle * distBwCircles for circle in range(1, noOfCircles + 1)]:
            pygame.draw.circle(self.surf, circleColor, self.radarCenter, radar, circleWidth)

        pygame.draw.line(self.surf, circleColor, (self.radarCenter[0], self.radarCenter[1] + radarRadius), (self.radarCenter[0], self.radarCenter[1] - radarRadius))
        pygame.draw.line(self.surf, circleColor, (self.radarCenter[0] + radarRadius, self.radarCenter[1]), (self.radarCenter[0] - radarRadius, self.radarCenter[1]))
         
        lineX = self.radarCenter[0] + lineLen * math.cos(math.radians(self.lineAngle))
        lineY = self.radarCenter[1] + lineLen * math.sin(math.radians(self.lineAngle))

        pygame.draw.line(self.surf, lineColor, self.radarCenter, (lineX, lineY), lineWidth)

        self.screen.blit(self.surf, (self.simWidth, 0))

    def update(self):
        self.lineAngle = (self.lineAngle + lineRotationSpeed / frameRate) % 360