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
        self.blips = []

    def draw(self):
        self.surf.fill((0, 0, 0, lineTrailAlpha), special_flags=BLEND_RGBA_MULT)
        for radar in [circle * distBwCircles for circle in range(1, noOfCircles + 1)]:
            pygame.draw.circle(self.surf, circleColor, self.radarCenter, radar, circleWidth)

        pygame.draw.line(self.surf, circleColor, (self.radarCenter[0], self.radarCenter[1] + radarRadius), (self.radarCenter[0], self.radarCenter[1] - radarRadius))
        pygame.draw.line(self.surf, circleColor, (self.radarCenter[0] + radarRadius, self.radarCenter[1]), (self.radarCenter[0] - radarRadius, self.radarCenter[1]))
         
        lineX = self.radarCenter[0] + lineLen * math.cos(math.radians(self.lineAngle))
        lineY = self.radarCenter[1] + lineLen * math.sin(math.radians(self.lineAngle))

        for blip in self.blips:
            self.drawBlip(blip)

        pygame.draw.line(self.surf, lineColor, self.radarCenter, (lineX, lineY), lineWidth)
        self.screen.blit(self.surf, (self.simWidth, 0))

    def drawBlip(self, blip):
        currentTime = pygame.time.get_ticks()
        dotX = self.radarCenter[0] + blipDistanceCenter * math.cos(math.radians(blip['angle']))
        dotY = self.radarCenter[1] + blipDistanceCenter * math.sin(math.radians(blip['angle']))
        elapsed_time = currentTime - blip['timer']

        if elapsed_time < fade_duration:
            alpha = abs(math.sin(blink_speed * elapsed_time / 1000))* 255
            blip['surf'].set_alpha(alpha)
             
            self.surf.blit(blip['surf'], (dotX, dotY))
        else:
            self.blips.remove(blip)
              
    def addBlip(self, angle):
        redDotImage = pygame.image.load("./assets/images/reddot1.png")
        redDotImage = pygame.transform.scale(redDotImage, (50, 50))
        self.blips.append({
            'surf': redDotImage,
            'angle': angle,
            'timer': pygame.time.get_ticks()
        })   
             
    def update(self):
        self.lineAngle = (self.lineAngle + lineRotationSpeed / frameRate) % 360