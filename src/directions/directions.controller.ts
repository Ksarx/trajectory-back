import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  Query,
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

  // @Get('directions')
  // findAll(@Query('faculty') faculty?: string): Promise<Direction[]> {
  //   return this.directionsService.findAll(faculty);
  // }

  @Get('jobs/:id/directions')
  async getDirections(
    @Param('id') id: string,
    @Query('faculty') faculty: string,
    @Query('page') page = 1,
    @Query('limit') limit = 6,
  ): Promise<any> {
    return this.directionsService.getDirections(+id, faculty, page, limit);
  }

  @Get('jobs/:id/directions/all')
  async getAllDirections(@Param('id') id: string): Promise<any> {
    return this.directionsService.getAllDirections(+id);
  }

  @Get('directions/:id')
  findOne(@Param('id') id: string): Promise<Direction> {
    return this.directionsService.findOne(+id);
  }

  // @Get('jobs/:id/directions')
  // findJobDirections(@Param('id') id: string): Promise<Direction[]> {
  //   return this.directionsService.findJobDirections(+id);
  // }

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
