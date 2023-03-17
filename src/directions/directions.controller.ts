import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { DirectionsService } from './directions.service';
import { CreateDirectionDto } from './dto/create-direction.dto';
import { UpdateDirectionDto } from './dto/update-direction.dto';
import { Direction } from './schemas/direction.schema';

@Controller()
export class DirectionsController {
  constructor(private readonly directionsService: DirectionsService) {}

  @Post('directions')
  create(@Body() createDirectionDto: CreateDirectionDto): Promise<Direction> {
    return this.directionsService.create(createDirectionDto);
  }

  @Get('directions')
  findAll(): Promise<Direction[]> {
    return this.directionsService.findAll();
  }

  @Get('directions/:id')
  findOne(@Param('id') id: string): Promise<Direction> {
    return this.directionsService.findOne(+id);
  }

  @Get('jobs/:id/directions')
  findJobDirections(@Param('id') id: string): Promise<Direction[]> {
    return this.directionsService.findJobDirections(+id);
  }

  @Patch('directions/:id')
  update(
    @Param('id') id: string,
    @Body() updateDirectionDto: UpdateDirectionDto,
  ): Promise<Direction> {
    return this.directionsService.update(+id, updateDirectionDto);
  }

  @Delete('directions/:id')
  remove(@Param('id') id: string): Promise<Direction> {
    return this.directionsService.remove(+id);
  }
}
